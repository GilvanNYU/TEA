import win32com.client as win32

class AspenVariables:
    def __init__(self, variables: dict[str,str], aspen: 'AspenSimulation'):
        self._vars = variables
        self._aspen = aspen

    def getter(self, name: str) -> float|int:
        return self._aspen.get_variable(self._vars[name])
    
    def setter(self, name: str, value: float|int) -> None:
        self._aspen.set_variable(self._vars[name], value)


class AspenSimulation:
    def __init__(self, full_path: str, 
                 variables: dict[str,str] = None, 
                 visibility=False):
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
        self._var = AspenVariables(variables, self) if variables != None else None

    @property
    def variables(self) -> AspenVariables:
        return self._var

    def get_variable(self, path: str) -> float|int:
        try:
            return self._aspen.Application.Tree.FindNode(path).Value
        except Exception as ex:
            print(f"Getting variable - {path}")
            self.quit()
            raise ex        
    
    def set_variable(self, path: str, value: float|int) -> None:
        try:
            self._aspen.Application.Tree.FindNode(path).Value = value
        except Exception as ex:
            print(f"Setting variable - {path}")
            self.quit()
            raise ex 
        
    def run_status(self) -> tuple[bool, str]:
        num_msg = self._aspen.Application.Tree.FindNode("\\Data\\Results Summary\\Run-Status\\Output\\PER_ERROR").Elements.Count
        if num_msg == 0:
            return (True, "Results available")
        else:
            msgs = []
            for i in range(int(num_msg/4)):
                type_msg = self._aspen.Application.Tree.FindNode(f"\\Data\\Results Summary\\Run-Status\\Output\\PER_ERROR\\{4*i + 2}").Value
                blocks = self._aspen.Application.Tree.FindNode(f"\\Data\\Results Summary\\Run-Status\\Output\\PER_ERROR\\{4*i + 3}").Value
                msgs.append(f"Results {type_msg}{blocks}")
            return  (False, "\n".join(msgs))
        
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



