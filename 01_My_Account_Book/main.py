from view import View
from Accounts_module import Account_Book, CRUD_Data

import os

Account_Book.make_file('my.xlsx')

while True:

    cursor = input(View.main()+'\n입력: ')

    if cursor == '1':
        file = input(View.load_account()+'\n입력: ')

        if file in os.listdir(os.path.dirname(__file__)):
            BOOK = Account_Book(file)
            print(View.load_account_done('조회 성공'))

            while True:

                cursor2 = input(View.main()+'\n입력: ')

                if cursor2 == '2': 
                    Q = input(View.view_data()+'\n입력: ')

                    if Q == '모두':
                        result = BOOK.load_file(Q)
                        print(result)
                    
                    else:
                        Q = Q.split(',')
                        result = BOOK.load_file(*Q)
                        print(result)
                    
                    continue

                if cursor2 == '3':
                    create_data = input(View.create_data()+'\n입력: ').split(',')
                    obj = CRUD_Data(file, *create_data)
                    obj.save_file(obj.write_data())

                    print('등록 완료')
                    continue


                if cursor2 == '4':
                    drop_num = input(View.delete_data()+'\n입력: ')
                    create_data = input(View.create_data()+'\n입력: ').split(',')
                    obj = CRUD_Data(file, *create_data)
                    obj.save_file(obj.renew_data(int(drop_num)))
                    
                    print('변경 완료')
                    continue

                if cursor2 == '5':
                    drop_num = input(View.delete_data()+'\n입력: ')
                    obj = CRUD_Data(file, 0,0,0,0,0)
                    obj.save_file(obj.delete_data(int(drop_num)))

                    print('삭제 완료')
                    continue

                if cursor2 == '6':
                    print(View.unload_me())
                    break
            
            break

        else:
            print(View.load_account_done('조회 실패'))
            continue


    if cursor == '6':
        print(View.unload_me())
        break

    else:
        print('가계부를 먼저 불러와주세요.')