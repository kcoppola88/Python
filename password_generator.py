import sys
import secrets
import string

def gen_pass():
    while True:
        try:    
            pass_length = int(input('Please enter an integer between 8 and 12: '))        
            if pass_length < 8:
                print ("Not long enough. Please try again. \n")
                pass
            elif pass_length > 12:
                print ("Too long. Please try again. \n")
                pass
            else:
                alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*();'<>?"            
                password = ''.join(secrets.choice(alphabet) for i in range(pass_length))
                print (password + "\a")
                print ("\n")
                input('Please copy your password then press enter to exit. ')
                print ("\n")
                sys.exit()
        except ValueError:
            print("That was not an integer. Please try again. \n")
    
def main():
    while True:    
        print ("\n")    
        option = input('Welcome. Would you like to generate a password? Y/N: ').lower()
        if option == "n":
            print ("\n")
            sys.exit()    
        elif option == "y":
            gen_pass()
        else:
            print ("You did not enter a correct option. Please try again. \n")
            pass

if __name__ == "__main__":

    main()