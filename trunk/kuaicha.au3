#include <GUIConstantsEx.au3>
#include <WindowsConstants.au3>
#include <IE.au3>
#include <Constants.au3>
#RequireAdmin

Opt("TrayIconHide", 1)
_IEErrorHandlerRegister()
ProcessClose("kuaicha_svr.exe")

Local $pid = Run(@ScriptDir & "\kuaicha_svr.exe","", @SW_HIDE,$STDERR_CHILD + $STDOUT_CHILD)

Local $oIE = _IECreateEmbedded()


#Region ### START Koda GUI section ### Form=
$Form1 = GUICreate("快查英汉词典", 623, 449, 192, 114)
Local $ctlID = GUICtrlCreateObj($oIE, 10, 10, 600, 360)
$Button1 = GUICtrlCreateButton("前进", 144, 392, 97, 25)
$Button2 = GUICtrlCreateButton("后退", 32, 392, 97, 25)
GUICtrlSetState($ctlID,$GUI_HIDE)
$waiting= GUICtrlCreateLabel("正在初始化...",10, 10, 160, 36)

GUISetState(@SW_SHOW)
#EndRegion ### END Koda GUI section ###


Local $hr = _IENavigate($oIE, "http://localhost:8401/")

While _IEGetObjById($oIE, "word")==0
	Sleep(1000)
	If not ProcessExists("kuaicha_svr.exe") Then
		Run(@ScriptDir & "\kuaicha_svr.exe","", @SW_HIDE,$STDERR_CHILD + $STDOUT_CHILD)
	EndIf
	_IENavigate($oIE, "http://localhost:8401/")
WEnd
GUICtrlSetState($ctlID,$GUI_SHOW)
GUICtrlSetState($waiting,$GUI_HIDE)

While 1
	$nMsg = GUIGetMsg()
	Switch $nMsg
		Case $GUI_EVENT_CLOSE
			ConsoleWrite($pid)
			ProcessClose($pid)
			Exit
		Case $Button1
			_IEAction($oIE, "forward")
		Case $Button2
			_IEAction($oIE, "back")
	EndSwitch
WEnd

