## Init
from internal.runtime.init import main as ProgramInit
import sys
import os
if not ("!noinit" in sys.argv):
    if ProgramInit() != True:
        input("Init failed. Press RETURN to exit.")
        sys.exit(1)
else:
    os.system("cls")
    print("starting...")

os.chdir("C:/")


## Configuration
ProgramTitle = "Video Compressor"
ThisVersion = "alpha"

## Imports
import colorama
from colorama import Fore, Back, Style
import json
import traceback
from tkinter import filedialog

from internal.libraries.utils import UserInput
import internal.libraries.compressor as compressor
import internal.runtime.update as update

## Variables
Login = os.getlogin() # notice: this just gets your local username (to be displayed in the input prefix)
Dir = os.path.dirname(__file__)
DataFile = f"{Dir}\\internal\\persistent\\Data.json"
LoadedFile = ""

## Functions
    
# Out
def Error(Message: str):
    print(Style.BRIGHT + Fore.RED + "error" + Style.RESET_ALL + ": " + str(Message))

def PrintSuccess(Message: str):
    print(Fore.LIGHTGREEN_EX + "success" + Fore.RESET + ": " + str(Message))

def Notice(Message: str):
    print(Style.BRIGHT + Fore.MAGENTA + "notice" + Style.RESET_ALL + ": " + str(Message))

def Warning(Message: str):
    print(Style.BRIGHT + Fore.YELLOW + "warning" + Fore.RESET + Style.RESET_ALL + ": " + str(Message))

def CustomException(Message: str):
    print(Fore.LIGHTRED_EX + str(Message) + Fore.RESET)

def ExceptionWithTraceback(e):
    Name = type(e).__name__

    print(f"\n{Style.BRIGHT}{Fore.RED}{Name}: {str(e)}{Style.RESET_ALL}")
    print(f"\n{Style.BRIGHT}{Fore.LIGHTCYAN_EX}Stack begin{Style.NORMAL}{Fore.LIGHTBLUE_EX}\n{traceback.format_exc()}{Fore.LIGHTCYAN_EX}{Style.BRIGHT}Stack end{Style.RESET_ALL}\n")
            

def ClearWindow():
    os.system("cls")

## Data
def Data_Set(NewData: dict) -> bool:
    try:
        with open(DataFile, "w") as File:
            File.write(json.dumps(NewData))
    except:
        return False
    else:
        return True

def Data_Read() -> dict | None:
    try:
        with open(DataFile, "r") as File:
            return json.loads(File.read())
    except Exception as e:
        # Warning(f"Failed to read data: {e}")
        # Pause()
        return None

# Other
def init():
    colorama.init()

def GetInputPrefix(Process: str = "Main", Instruction: str = None) -> str:
    if Instruction != None:
        Instruction = f"{Fore.RESET}: {Fore.LIGHTBLUE_EX}{Instruction}\n{Fore.BLUE}> {Fore.RESET}"
    else:
        Instruction = f"\n{Fore.MAGENTA}$ {Fore.RESET}"

    return f"\n{Fore.GREEN}{Login}@{ProgramTitle}{Fore.RESET} {Style.DIM}~{Style.RESET_ALL} {Fore.YELLOW}{Process}{Instruction}"

def ParseInput(Query: str) -> tuple[bool, str, str]:
    try:
        Parts = Query.split(" ", 1)
        Command = Parts[0]
        Params = len(Parts) > 1 and Parts[1] or None
    except:
        return False, None, None
    else:
        return True, Command, Params

def Pause():
    os.system("pause")

def Quit(Message: str | None = None):
    if Message:
        CustomException(f"\n{Message}")
        print("\n\nThe program will now exit.")
        Pause()
        sys.exit(0)
    else:
        CustomException("\nQuitting...")
        sys.exit(0)

def FirstSetup():
    pass
    # try:
    #     Data = {
    #         "Update Token": None
    #     }

    #     ClearWindow()
    #     print("Performing first time setup...")
        
    #     while True:
    #         UpdateToken = input(GetInputPrefix("Setup", "Please enter the Update Authorisation Token, or Control+C to skip."))
    #         # UpdateToken = input("\nPlease enter the Update Authorisation Token\nControl+C to skip\n> ")
    #         print("Validating...")

    #         update.SetUpdateToken(UpdateToken)
    #         Ver = update.GetLatestVersionCode()

    #         if Ver == None:
    #             print("Either the wrong token has been entered, or there is a problem with your internet connection.")
    #         else:
    #             Data["Update Token"] = UpdateToken
    #             print("Access is granted!")
    #             Pause()
    #             break
        
    #     Data_Set(Data)
    #     ClearWindow()
    # except KeyboardInterrupt:
    #     pass
    # except Exception as e:
    #     ExceptionWithTraceback(e)
    #     Quit(f"Fatal error during setup!")


## Internal Commands
class Container_Commands:
    def load(_, Query: str):
        global LoadedFile
        
        if Query in ["", None]:
            Query = filedialog.askopenfile(title="Select a file to load")
            
            if Query == None:
                return print("Cancelled. No file was loaded.")
            else:
                Query = Query.name
        
        if not os.path.exists(str(Query)):
            Error("The path specified does not exist.")
        else:
            LoadedFile = Query
            return

    def compress(_, args: str):
        global LoadedFile
        if LoadedFile == "":
            return Error("A file is not loaded. Use the \"load\" command to do so.")
        
        if args == None:
            args = ""

        ## Parse
        TargetSize = OutputPath = None
        args = args.split(" ", 1)

        if len(args) == 2:
            TargetSize = args[0]
            OutputPath = args[1]
        else:
            try:
                TargetSize = input(GetInputPrefix("compress", "Enter target file size (in MB)"))
                OutputPath = input(GetInputPrefix("compress", "Enter output file path, or \"browse\""))
            except KeyboardInterrupt:
                return print()

        ## Validate
        InputExtension = os.path.splitext(LoadedFile)[1]

        try:
            TargetSize = float(TargetSize)
        except ValueError:
            return Error(f"The target file size, {TargetSize}, cannot be recognised as a number.")
        
        if OutputPath == "browse":
            OutputPath = filedialog.asksaveasfile(title="Select the output file path", defaultextension=InputExtension)

            if OutputPath == None:
                return print("Cancelled.")
            else:
                OutputPath = OutputPath.name
                
        if not os.path.exists(OutputPath):
            Error("The provided output path does not exist!")
        else:
            print("starting compression...")

            Success, Result = compressor.CompressVideo(f"\"{LoadedFile}\"", OutputPath, TargetSize)

            if Success:
                print("The file was compressed successfully.")
            else:
                Error(f"Compression failed!\n{type(Result).__name__}: {str(e)}")

    def update(*_):
        print("Preparing to update...")
        Latest = update.GetLatestVersionCode()

        if Latest == None:
            return Error("Could not get latest version. Check your update token.")
        elif Latest == ThisVersion:
            Warning(f"You are already using the latest version available, {Fore.LIGHTGREEN_EX}{ThisVersion}{Fore.RESET}.")

            if not UserInput.YesNo("Do you want to update anyway?"):
                return
        else:
            print(f"You are about to upgrade to the latest version, {Fore.LIGHTGREEN_EX}{ThisVersion}{Fore.RESET}.")
            if not UserInput.YesNo("Do you want to continue?"):
                return

        ClearWindow()
        update.Update(Dir)

## Runtime
Commands = Container_Commands()

def main():

    ## Init
    ClearWindow()
    print("setting up...")

    init()

    ## Retrieve latest version code 
    ClearWindow()
    print("checking for updates...")
    
    LatestVer = update.GetLatestVersionCode()

    ## Greeting
    ClearWindow()
    print(f"{ProgramTitle} [Version {ThisVersion}]")
    print(f"Control+C to exit\n")

    ## Ensure that file version code & current version code (stored in Configuration) are the same
    try:
        Ver = open(f"{Dir}\\internal\\VERSION.txt", "r")
        if Ver.readable():
            FileVer = Ver.read().replace("\n", "")
            if FileVer != ThisVersion:
                Warning(f"Mismatch between program version and file version! {ThisVersion = } != {FileVer = }")
        Ver.close() 
    except Exception as e:
        Warning(f"Failed to read {Dir}\\internal\\VERSION.txt file: {e}")

    if ThisVersion != LatestVer and LatestVer != None:
        Notice(f"An update is available! Run \"{Fore.BLUE}update{Fore.RESET}\" to download the latest version. ({Fore.LIGHTRED_EX}{ThisVersion}{Fore.RESET} -> {Fore.GREEN}{LatestVer}{Fore.RESET})")
    
    # if Data.get("Update Token", None) == None:
    #     Warning(f"Missing update token! Run the \"{Fore.BLUE}init{Fore.RESET}\" command or restart the program to enter one.")

    if LatestVer == None:
        Warning("Failed to get latest update! Please check your internet connection.")

    ## Set the updater's update token
    Data = Data_Read() or {}
    update.SetUpdateToken(Data.get("Update Token", None))

    ## Command line loop
    while True:
        try:
            Query = input(GetInputPrefix())
        except KeyboardInterrupt:
            Quit()
        else:
            print()
            Valid, Command, Params = ParseInput(Query)

            if not Valid or Command == "":
                continue

            ## Get the method
            Method = getattr(Commands, Command, None)

            if callable(Method):
                try:
                    Method(Params)
                except Exception as e:
                    CustomException(f"\nAn exception ocurred whilst running the command \"{Command}\"!")
                    ExceptionWithTraceback(e)
            else:
                CustomException(f"\"{Command}\" is not recognised as an internal command.")

if __name__ == "__main__":
    CatchErrors = True ## Debug flag

    if CatchErrors:
        try:
            main()
        except KeyboardInterrupt:
            Quit()
        except EOFError:
            Quit()
        except Exception as e:
            if e == "" or e == None:
                e = "Unknown exception"

            CustomException(f"\nA fatal error ocurred during runtime! The program will now exit. See details below.\n\n")
            ExceptionWithTraceback(e)
            Pause()
    else:
        ClearWindow()
        Warning("Errors will be uncaught!\n")
        Pause()
        main()
    