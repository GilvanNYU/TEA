import win32com.client as win32

class AspenEngine:
    def __init__(self, full_path: str, visibility= False):
        self._file_path = full_path
        msg = ""
        try:
            msg = "Creating Aspen Plus instance"
            self._aspen = win32.gencache.EnsureDispatch("Apwn.Document")
            msg = f"Opening Aspen Plus simulation - {self._file_path}"
            self._aspen.InitFromArchive2(self._file_path)
            self._aspen.Visible = visibility
        except Exception as ex:
            print(msg)
            self.quit()
            raise ex
    
    def visible(self, value: bool) -> None:
        self._aspen.Visible = value
        
    def run(self) -> None:
        self._aspen.Engine.Run2()

    def reinitiate(self) -> None:
        self._aspen.Reinit()

    def quit(self) -> None:
        self._aspen.Application.Quit()

    def find_node(self, path: str):
        try:
            return self._aspen.Application.Tree.FindNode(path)
        except Exception as ex:
            print(f"Invalid path - {path}")
            self.quit()
            raise ex 
        
    def get_variable(self, path: str) -> float|int:
        return self.find_node(path).Value
    
    def set_variable(self, path: str, value: float|int) -> None:
        self.find_node(path).Value = value

    def run_status(self) -> tuple[bool, str]:
        code = self.find_node('\\Data\\Results Summary\\Run-Status\\Output\\UOSSTAT2').Value
        status = True if code == 8 else False

        path = "\\Data\\Results Summary\\Run-Status\\Output\\PER_ERROR"
        num_msg = self.find_node(path).Elements.Count
        if num_msg == 0:
            return (status, "No message.")
        else:
            msgs = []
            for i in range(1, num_msg+1):
                msgs.append(self.find_node(path + f"\\{i}").Value)
            return  (status, "\n".join(msgs))