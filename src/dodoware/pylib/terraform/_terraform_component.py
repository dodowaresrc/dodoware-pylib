import jinja2
import json
import logging

from dodoware.pylib.proc import ProcessRunner, ProcessStatus, StreamSettings
from dodoware.pylib.util import chdir_context

from dodoware.pylib.terraform._terraform_tags import TerraformTags
from dodoware.pylib.terraform._terraform_folder import TerraformFolder
from dodoware.pylib.terraform._terraform_counts import TerraformCounts

class TerraformComponent(TerraformFolder):
    """
    A terraform component folder.
    """

    def __init__(self, project, name, no_backend=False):

        super().__init__(project.logger, name, project.get_path(name))

        self.project = project

        self.no_backend = no_backend

        self.prefix = "terraform"

        self.vars_template = f"{self.prefix}.vars.j2"
        self.vars_file = f"{self.prefix}.vars"
        self.backend_template = f"{self.prefix}.backend.j2"
        self.backend_file = f"{self.prefix}.backend"
        self.plan_file = f"{self.prefix}.plan"
        self.counts_file = f"{self.prefix}.counts"

    def prepare(self, environment:str, region:str, color:str, extra_vars=None):
        """
        Create the `vars` and `backend` files by rendering J2 templates.
        """

        tags = TerraformTags.new(
            project=self.project.project_info.project,
            short_project=self.project.project_info.short_project,
            component=self.name,
            environment=environment,
            region=region,
            color=color)

        template_vars = dict(extra_vars) if extra_vars else {}

        template_vars.update(tags.dict())

        self.check_file(self.vars_template, exist=True)

        self.check_file(self.vars_file, exist=False)

        self.check_file(self.backend_template, exist=(not self.no_backend))

        self.check_file(self.backend_file, exist=False)

        j2_loader = jinja2.FileSystemLoader(searchpath=self.folder)

        j2_environment = jinja2.Environment(loader=j2_loader)

        j2_template = j2_environment.get_template(self.vars_template)

        with open(self.get_path(self.vars_file), mode="w", encoding="UTF-8") as f:
            f.write(j2_template.render(template_vars))

        if self.no_backend:
            return

        j2_template = j2_environment.get_template(self.backend_template)

        with open(self.get_path(self.backend_file), mode="w", encoding="UTF-8") as f:
            f.write(j2_template.render(template_vars))

    def run_terraform(self, phase, args, prev=None):
        """
        Change into the component folder, run Terraform, then
        change back to the original folder.

        Args:
            phase (str):
                The terraform phase being run.
            args (List[str]):
                Terraform arguments (not including the Terraform program).
            prev (str):
                The previous Terraform phase.  If set, make sure the previous
                phase ran successfully before running Terraform.
        """

        args = ["terraform"] + (args or [])

        if prev:
            self.check_file(self.get_phase_stdout_file(prev), exist=True)
            self.check_file(self.get_phase_stderr_file(prev), exist=True)
            self.check_file(self.get_phase_status_file(prev), exist=True)
            status = self.get_phase_status(prev)
            if status.return_code != 0:
                raise RuntimeError(f"previous phase was not successful: {prev}")

        with chdir_context(self.folder):
            self._run_terraform(phase, args)

    def _run_terraform(self, phase, args):
        """
        Run Terraform.
        """

        self.logger.debug("phase=%s", phase)

        self.logger.debug("args=%s", args)

        stdout_settings = StreamSettings(
            outfile = self.get_phase_stdout_file(phase),
            logger = self.logger,
            log_level = logging.INFO,
            log_prefix = f"{phase} stdout: "
        )

        stderr_settings = StreamSettings(
            outfile = self.get_phase_stderr_file(phase),
            logger = self.logger,
            log_level = logging.INFO,
            log_prefix = f"{phase} stderr: "
        )

        process_runner = ProcessRunner(
            args=args,
            stdout_settings=stdout_settings,
            stderr_settings=stderr_settings)

        process_runner.start()

        process_runner.join()

        status = process_runner.get_status()

        status_file = self.get_phase_status_file(phase)

        with open(status_file, mode="w", encoding="UTF-8") as f:
            json.dump(status.dict(), f, indent=4, sort_keys=True)

        if status.return_code != 0:
            raise RuntimeError(
                f"terraform failed: return_code={status.return_code} args={args}"
            )

    def get_phase_stdout_file(self, phase):
        """
        Get the stdout file for a terraform phase.

        Args:
            phase (str):
                The terraform phase.

        Returns:
            str:
                The stdout file for the input phase.
        """

        return f"{self.prefix}-{phase}.stdout"

    def get_phase_stderr_file(self, phase):
        """
        Get the stderr file for a terraform phase.

        Args:
            phase (str):
                The terraform phase.

        Returns:
            str:
                The stderr file for the input phase.
        """

        return f"{self.prefix}-{phase}.stderr"

    def get_phase_status_file(self, phase):
        """
        Get the status file for a terraform phase.

        Args:
            phase (str):
                The terraform phase.

        Returns:
            str:
                The status file for the input phase.
        """

        return f"{self.prefix}-{phase}.status"

    def get_phase_status(self, phase):
        """
        Load the status file for a terraform phase.
        The status file must exist.

        Args:
            phase (str):
                The terraform phase.

        Returns:
            TerraformStatus:
                Terraform status loaded from the status file.
        """

        status_file = self.get_phase_status_file(phase)

        self.check_file(status_file, exist=True)

        status_path = self.get_path(status_file)

        with open(status_path, mode="r", encoding="UTF-8") as f:
            status_dict = json.load(f)

        return ProcessStatus(**status_dict)

    def init1(self):
        """
        Run `terraform init` with no backend.  This is just to get the modules
        initialzed locally so we can run `terraform validate` without needing
        a connection to backend storage.
        """

        self.check_file(self.vars_file, exist=True)

        self.check_file(self.backend_file, exist=(not self.no_backend))

        args = ["init", "-backend=false", "-no-color"]

        self.run_terraform("init1", args)

    def validate(self):
        """
        Run `terraform validate`.
        """

        args = ["validate", "-no-color"]

        self.run_terraform("validate", args, prev="init1")

    def init2(self):
        """
        Run `terraform init`.  This will connect to backend storage.
        """

        args = ["init", "-no-color"]

        if not self.no_backend:
            args.append(f"-backend-config={self.backend_file}")

        self.run_terraform("init2", args, prev="validate")

    def plan(self):
        """
        Run `terraform plan`.
        """

        args = [
            "plan",
            "-no-color",
            f"-var-file={self.vars_file}",
            "-input=false",
            f"-out={self.plan_file}"]

        self.run_terraform("plan", args, prev="init2")

        stdout_file = self.get_phase_stdout_file("plan")

        stdout_path = self.get_path(stdout_file)

        terraform_counts = TerraformCounts.load(stdout_path)

        with open(self.get_path(self.counts_file), mode="w", encoding="UTF-8") as f:
            json.dump(terraform_counts.dict(), f, indent=4, sort_keys=True)

    def apply(self, allow_destroy=False, allow_change=False):
        """
        Run `terraform apply`.

        Args:
            allow_destroy (bool):
                Allow Terraform to destroy resources.  Default is `False`.
            allow_change (bool):
                Allow Terraform to change resources.  Default is `False`.
        """

        self.check_file(self.counts_file, exist=True)

        self.check_file(self.plan_file, exist=True)

        with open(self.get_path(self.counts_file), mode="r", encoding="UTF-8") as f:
            data = json.load(f)

        counts = TerraformCounts(**data)

        if counts.destroy and not allow_destroy:
            raise RuntimeError("destroy count is not zero and `allow_destroy` not set")

        if counts.change and not allow_change:
            raise RuntimeError("change count is not zero and `allow_change` not set")


        args = [
            "apply",
            "-no-color",
            "-input=false",
            "-auto-approve",
            self.plan_file
        ]

        self.run_terraform("apply", args, prev="plan")
