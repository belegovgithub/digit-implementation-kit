from common import *
from config import config
import io
import os 
from  processing import process_bank_details
def main():
    bank = process_bank_details.bank()    
    #replaceNone(bank,None,null)
    bankbranch = process_bank_details.bankbranch(bank)
    accountcodepurpose = process_bank_details.accountcodepurpose()
    chartaccount = process_bank_details.chartaccount(accountcodepurpose)
    fund = process_bank_details.fund()
    bankaccount = process_bank_details.bankaccount(bankbranch, chartaccount, fund)
    print(bankaccount)   

if __name__ == "__main__":
    main()
