# Copyright (c) 2024, UCL實驗室 and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document

class UCL_HR(Document):
    def before_insert(self):
        # 如果員工ID字段为空，生成新的員工ID
        if not self.employee_id:
            self.employee_id = self.get_new_employee_id()

    def get_new_employee_id(self):
        # 獲取最新的員工ID
        last_employee_id = frappe.db.get_value(
            "UCL_HR",  # 對應的 DocType 名稱
            filters={},
            fieldname="employee_id",
            order_by="employee_id desc"
        )

        if last_employee_id:
            # 解析最後一個員工ID中的數字部分
            last_number = int(last_employee_id.split('_')[1])
            new_number = last_number + 1
        else:
            new_number = 1

        # 返回新生成的員工ID，格式為 HR_00001
        return "HR_{:05d}".format(new_number)

    def validate(self):
      # 在文檔驗證階段設置「職位ID」
        self.set_position_id()

        # 根據職位自動填寫對應的部門
        self.set_department()


    def set_position_id(self):
        # 職位與職位ID對應表
        position_map = {
            "工程部-組員": "staff",
            "經理": "rest-admin",
            "副總": "admin"
        }

        # 根據「職位」設置「職位ID」
        if self.position in position_map:
            self.position_id = position_map[self.position]
        else:
            # 如果選擇了未定義的職位，職位ID設置為null
            self.position_id = "待設定"


    def set_department(self):
        # 職位對應部門的映射表
        position_department_map = {
            "經理": "管理部門",
            "副總": "管理部門",
            "工程部-A組長": "工程部",
            "工程部-B組長": "工程部",
            "工程部-組員": "工程部",
            "業務主管": "業務部",
            "業務助理": "業務部",
            "會計": "行政部",
            "倉管": "倉儲部"
        }

        # 根據「職位」填寫對應的「部門」
        if self.position in position_department_map:
            self.department = position_department_map[self.position]
        else:
            frappe.throw(f"{self.position}")
