import win32com.client as win32

class AspenSimulation:
    def __init__(self, full_path: str, visibility=False):
        self._file_path = full_path
        msg = ""
        try:
            msg = "Creating Aspen Plus instance"
            self._aspen = win32.gencache.EnsureDispatch("Apwn.Document")
            msg = f"Opening Aspen Plus simulation - {self._file_path}"
            self._aspen.InitFromArchive2(self._file_path)
            self.aspen.Visible = visibility
        except Exception as ex:
            print(msg)
            self.quit()
            raise ex

    def get_variable(self, path: str) -> float|int:
        try:
            return self.aspen.Application.Tree.FindNode(path).Value
        except Exception as ex:
            print(f"Getting variable - {path}")
            self.quit()
            raise ex        
    
    def set_variable(self, path: str, value: float|int) -> None:
        try:
            self.aspen.Application.Tree.FindNode(path).Value = value
        except Exception as ex:
            print(f"Setting variable - {path}")
            self.quit()
            raise ex 
        
    def simulation_status(self) -> bool:
        status = self.aspen.Application.Tree.FindNode("\\Data\\Results Summary\\Run-Status\\Output\\PER_ERROR").Elements.Count
        if status == 0:
            return True
        else:
            return  False
        
    def run(self) -> None:
        self._aspen.Engine.Run2()

    def reinitiate(self) -> None:
        self._aspen.Reinit()

    def visible(self, value: bool) -> None:
        self._aspen.Visible = value

    def quit(self) -> None:
        self._aspen.Application.Quit()

    def __del__(self) -> None:
        self.quit()