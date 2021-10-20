#include <ButtonConstants.au3>
#include <WindowsConstants.au3>
#include <GUIConstantsEx.au3>
#include <WinAPI.au3>
#include <Array.au3>

$hGui = GUICreate("Super Secret Login", 352, 109, -1, -1)
GUISetFont(9, 400, 0, "Courier New")
$hLabel = GUICtrlCreateLabel("Enter Password:", 25, 25, 109, 18)
$hInput = GUICtrlCreateInput("", 140, 23, 188, 20)
GUICtrlSetFont(-1, 9, 400, 0, "Courier New", 5)
$hButton = GUICtrlCreateButton("Login!", 122, 71, 109, 25)
GUICtrlSetStyle(-1, $BS_FLAT)
$hCaret = _WinAPI_CreateCaret($hGui, 10, 2)
$mServerKey = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
_WinAPI_ShowCaret($hGui)
GUISetState()

While 1
	$hMsg = GUIGetMsg()
	Switch $hMsg
		Case $GUI_EVENT_CLOSE
			Exit
        Case $hButton
            OnClick()
	EndSwitch
WEnD

Func OnClick()
    Local $text = GUICtrlRead($hInput)
    Local $fuckPython = StringLen($text)
    If $fuckPython == 0 Then Return
    Local $oldFuck = $fuckPython
    GUICtrlSetState($hButton, $GUI_DISABLE)
    Local $fuck = FuckIt($text, $mserverKey)
    GUICtrlSetState($hButton, $GUI_ENABLE)
    $fuckPython = "7188bb1563e5702342e22a856ad3df1cfa9729b4115d8cfb1f07a0c6fc916477f02f77d656834379b32e"
    if String(BinaryToString($fuck)) == ("" & $fuckPython) Then
        MsgBox(0x40, "Good Job!", "Read the instructions and see if you can submit It!", 0, $hGui)
    Else
        MsgBox(0x40, ":(", "You have a long way to go buddy!" & @crlf & ":(", 0, $hGui)
    Endif
EndFunc

Func FuckIt($Data, $Key)
	Local $Opcode = "0x5589e56031c081ec00010000880404403d0001000075f531f631db0fb6043401c389f0b92b00000031d2f7f18b45140fbe0c1001cb0fb6db8a0c348a041c880434880c1c83c60181fe0001000075cc31f631d231c942460fb6d28a041401c10fb6c98a1c0c88040c881c1400d80fb6c08b7d0c8a5c37ff8a040431c38b7d08e8100000003b751075cc81c40001000061c9c210005053eb1858c1eb048a1c18885c77fe5b83e30f8a1c18885c77ff58c3e8e3ffffff30313233343536373839616263646566"
	Local $CodeBuffer = DllStructCreate("byte[" & BinaryLen($Opcode) & "]")
	DllStructSetData($CodeBuffer, 1, Binary($Opcode))

	Local $Buffer = DllStructCreate("byte[" & StringLen($Data) & "]")
	DllStructSetData($Buffer, 1, $Data)

    Local $destBuffer = DllStructCreate("char[" & (StringLen($Data)*2+1) & "]")

	DllCall("user32.dll", "none", "CallWindowProc", "ptr", DllStructGetPtr($CodeBuffer), _
													"ptr", DllStructGetPtr($destBuffer), _
                                                    "ptr", DllStructGetPtr($Buffer), _
													"int", StringLen($Data), _
													"str", $Key)

	Local $Ret = DllStructGetData($destBuffer, 1)
	$Buffer = 0
	$CodeBuffer = 0
	Return $Ret
EndFunc