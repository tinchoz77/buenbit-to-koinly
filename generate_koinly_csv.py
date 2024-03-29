from Koinly import *
import openpyxl

report = KoinlyCustomFile()

# Lists expected operation types and if the operation is reported in two lines
buenbit_operations = {"CONVERSION": True,
                      "DEPOSITO": False,
                      "RETIRO": False,
                      "TRANSFERENCIA P2P RECIBIDA": False,
                      "CONSUMO DE TARJETA": False,
                      "AJUSTE DE TARJETA": False,
                      "CASHBACK": False}

# Define variable to load the buenbit report
xls = openpyxl.load_workbook("buenbit_sample_report.xlsx").active

# Loop through every transaction (assuming there's not any failed trx)
# TODO: Check for FAILED status 
for row_num in range(2, xls.max_row+1):
    print(f"Line {row_num}: ", end = "")
    xls_moneda = xls.cell(row=row_num, column=5).value
    xls_monto = xls.cell(row=row_num, column=6).value
    xls_costored = xls.cell(row=row_num, column=7).value

    if xls.cell(row=row_num, column=1).value is None:
        # complete previous transaction
        xls_operation = last_operation
        trx.set_amount(xls_monto, xls_moneda)
        trx.set_cost(xls_costored, xls_moneda)

        print(f"completing Id: {xls_id} - Operacion: {xls_operation}")
        if buenbit_operations[xls_operation]:
            report.add_trx(trx)

    else:
        # new transaction
        xls_date = xls.cell(row=row_num, column=1).value
        xls_id = xls.cell(row=row_num, column=2).value
        xls_operation = xls.cell(row=row_num, column=3).value
        last_operation = xls_operation

        if not xls_operation in buenbit_operations:
            raise Exception(f"Operation {xls_operation} not defined")
        
        print(f"Id: {xls_id} - Operacion: {xls_operation}")
        trx = KoinlyCustomTransaction(xls_id, xls_date, xls_operation)
        trx.set_amount(xls_monto, xls_moneda)
        trx.set_cost(xls_costored, xls_moneda)

        if not buenbit_operations[xls_operation]:
            report.add_trx(trx)

# Export koinly csv file
print("Writing file...", end = "")
report.write("buenbit_koinly_report.csv")
print(" done.")