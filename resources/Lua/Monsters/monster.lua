-- A basic monster script skeleton you can copy and modify for your own creations.
comments = { {{comments}} } -- {"Smells like the work\rof an enemy stand.", "Poseur is posing like his\rlife depends on it.", "Poseur's limbs shouldn't be\rmoving in this way."}
commands = { {{commands}} } -- {"Act 1", "Act 2", "Act 3"}
randomdialogue = { {{randomdialogue}} } -- {"Random\nDialogue\n1.", "Random\nDialogue\n2.", "Random\nDialogue\n3."}

sprite = "{{sprite}}" -- "poseur" --Always PNG. Extension is added automatically.
name = "{{name}}" -- "Poseur"
hp = {{hp}} -- 100
atk = {{atk}} -- 1
def = {{defense}} -- 1
check = "{{check}}" -- "Check message goes here."
dialogbubble = "{{dialogbubble}}" -- "right" -- See documentation for what bubbles you have available.
canspare = {{canspare}} -- false
cancheck = {{cancheck}} -- true

-- Happens after the slash animation but before
function HandleAttack(attackstatus)
    if attackstatus == -1 then
        -- player pressed fight but didn't press Z afterwards
    else
        -- player did actually attack
    end
end

-- This handles the commands; all-caps versions of the commands list you have above.
function HandleCustomCommand(command)
    if command == "ACT 1" then
        currentdialogue = {"Selected\nAct 1."}
    elseif command == "ACT 2" then
        currentdialogue = {"Selected\nAct 2."}
    elseif command == "ACT 3" then
        currentdialogue = {"Selected\nAct 3."}
    end
    BattleDialog({"You selected " .. command .. "."})
end
