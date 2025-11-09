from src.view.AbstractMenu import AbstractMenu


class MainMenu(AbstractMenu):
    def __init__(self):
        main_menu_options = \
            {1: "EC2 Instances",
             2: "EBS Storage",
             3: "S3 Storage",
             4: "Monitoring",
             5: "RDS Databases",
             99: "Exit"}

        super().__init__("Main Menu", main_menu_options)

    def execute_choice(self, choice):
        if choice == 1:
            self.open_ec2_menu()
        elif choice == 2:
            self.open_ebs_menu()
        elif choice == 3:
            self.open_s3_menu()
        elif choice == 4:
            self.open_monitoring_menu()
        elif choice == 5:
            self.open_rds_menu()
        elif choice == 99 or choice == 0:
            self.exit_application()
        else:
            self.handle_invalid_choice()

        return True

    def open_ec2_menu(self):
        from src.view.ec2_menu import EC2Menu
        ec2_menu = EC2Menu()
        ec2_menu.run()

    def open_ebs_menu(self):
        from src.view.ebs_menu import EBSMenu
        ebs_menu = EBSMenu()
        ebs_menu.run()

    def open_s3_menu(self):
        from src.view.s3_menu import S3Menu
        s3_menu = S3Menu()
        s3_menu.run()

    def open_monitoring_menu(self):
        from src.view.cw_menu import CloudWatchMenu
        cw_menu = CloudWatchMenu()
        cw_menu.run()

    def open_rds_menu(self):
        from src.view.rds_menu import RDSMenu
        rds_menu = RDSMenu()
        rds_menu.run()
