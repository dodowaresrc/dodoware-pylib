from dodoware.pylib.cmd import Command, CommandTool, DictAction
from dodoware.pylib.terraform._terraform_project import TerraformProject

class PrepareCommand(Command):

    def __init__(self, tool):

        super().__init__(tool, "prepare", "prepare terraform input files")

    def init_syntax(self):

        self.rg.add_argument(
            "--project_folder",
            required=True,
            help="path to the project folder")

        self.rg.add_argument(
            "--environment",
            required=True,
            help="the deployment environment")

        self.rg.add_argument(
            "--region",
            required=True,
            help="the deployment region")

        self.rg.add_argument(
            "--component",
            required=True,
            help="the component being deployed")

        self.rg.add_argument(
            "--color",
            required=True,
            help="the deployment color")

        self.parser.add_argument(
            "--extra_var",
            action=DictAction,
            help="set extra input vars"
        )

    def handle_command(self, pr):

        project = TerraformProject(
            logger=self.logger,
            folder=pr.project_folder)

        component = project.get_component(pr.component)

        component.prepare(
            environment=pr.environment,
            region=pr.region,
            color=pr.color,
            extra_vars=pr.extra_var)

class Init1Command(Command):

    def __init__(self, tool):

        super().__init__(tool, "init1", "run 'terraform init' without backend")

    def init_syntax(self):

        self.rg.add_argument(
            "--project_folder",
            required=True,
            help="path to the project folder")

        self.rg.add_argument(
            "--component",
            required=True,
            help="the component being deployed")

    def handle_command(self, pr):

        project = TerraformProject(
            logger=self.logger,
            folder=pr.project_folder)

        component = project.get_component(pr.component)

        component.init1()

class ValidateCommand(Command):

    def __init__(self, tool):

        super().__init__(tool, "validate", "run 'terraform validate'")

    def init_syntax(self):

        self.rg.add_argument(
            "--project_folder",
            required=True,
            help="path to the project folder")

        self.rg.add_argument(
            "--component",
            required=True,
            help="the component being deployed")

    def handle_command(self, pr):

        project = TerraformProject(
            logger=self.logger,
            folder=pr.project_folder)

        component = project.get_component(pr.component)

        component.validate()

class Init2Command(Command):

    def __init__(self, tool):

        super().__init__(tool, "init2", "run 'terraform init' with backend")

    def init_syntax(self):

        self.rg.add_argument(
            "--project_folder",
            required=True,
            help="path to the project folder")

        self.rg.add_argument(
            "--component",
            required=True,
            help="the component being deployed")

    def handle_command(self, pr):

        project = TerraformProject(
            logger=self.logger,
            folder=pr.project_folder)

        component = project.get_component(pr.component)

        component.init2()

class PlanCommand(Command):

    def __init__(self, tool):

        super().__init__(tool, "plan", "run 'terraform plan'")

    def init_syntax(self):

        self.rg.add_argument(
            "--project_folder",
            required=True,
            help="path to the project folder")

        self.rg.add_argument(
            "--component",
            required=True,
            help="the component being deployed")

    def handle_command(self, pr):

        project = TerraformProject(
            logger=self.logger,
            folder=pr.project_folder)

        component = project.get_component(pr.component)

        component.plan()

class ApplyCommand(Command):

    def __init__(self, tool):

        super().__init__(tool, "apply", "run 'terraform apply'")

    def init_syntax(self):

        self.rg.add_argument(
            "--project_folder",
            required=True,
            help="path to the project folder")

        self.rg.add_argument(
            "--component",
            required=True,
            help="the component being deployed")

        self.parser.add_argument(
            "--allow_destroy",
            action="store_true",
            help="allow terraform to destroy resources")

        self.parser.add_argument(
            "--allow_change",
            action="store_true",
            help="allow terraform to change resources")

    def handle_command(self, pr):

        project = TerraformProject(
            logger=self.logger,
            folder=pr.project_folder)

        component = project.get_component(pr.component)

        component.apply(allow_destroy=pr.allow_destroy, allow_change=pr.allow_change)

class TerraformTool(CommandTool):

    @property
    def description(self):
        return "run terraform for a project component"

    def get_command_classes(self):
        return (
            PrepareCommand,
            Init1Command,
            ValidateCommand,
            Init2Command,
            PlanCommand,
            ApplyCommand
        )
