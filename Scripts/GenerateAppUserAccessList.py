from openpyxl import Workbook

from PowerPyAPI import Tenant

app_names = ['BI360', 'Hero Analytics', 'High End & Craft Sales Reporting V1', 'Canada Solutions',
             'Canada Commercial Sales Production', 'Ontario Field Sales', 'Supply Chain Analytics',
             'Ontario Sales Intelligence', 'S&OP for Growth - US', 'Canada Commercial Sales', 'Beyond Beer Canada',
             'Mill Street Commercial Sales', 'Prairies Commercial Sales', 'OnePortal', 'Beyond Beer Canada Commercial',
             'Logistics Executive Cockpit', 'Promo Analytics', 'Canada VC Targets', 'Atlantic Sales Intelligence',
             'Canada TBS Reports', 'Alchemy Datasets', 'Alchemy Dataflows']

illegal_excel_sheet_name_characters = ['[', ']']


def main():
    wb = Workbook()
    ws = wb.active
    tenant = Tenant.authenticate_by_file('../config.yaml')
    apps = tenant.get_apps_by_names(app_names, include_dev=True, include_test=True)
    for app in apps:
        users = app.get_app_users()
        app_name = app.name
        for char in illegal_excel_sheet_name_characters:
            app_name = app_name.replace(char, "")
        ws.title = app_name
        for user in users:
            ws.append([user.display_name, user.principal_type, user.app_user_access_right, user.email_address])
        ws = wb.create_sheet()

    wb.save('User Access.xlsx')


if __name__ == '__main__':
    main()


