# Creator: Tyler Johnson
# Date: 6/29/2016
# Name: create_users.ps1
# Description: Creates a kerberos service principal in AD and saves the keytab file

Import-Module ActiveDirectory
[System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") | Out-Null 
[System.Reflection.Assembly]::LoadWithPartialName("System.Drawing") | Out-Null 

Function Custom-Dialog($title,$prompt,$button1,$button2){
    $objForm = New-Object System.Windows.Forms.Form 
    $objForm.Text = "$title"
    $objForm.ShowIcon = $False
    $objForm.Size = New-Object System.Drawing.Size(320,150) 
    $objForm.StartPosition = "CenterScreen"
    $objForm.KeyPreview = $True
    $objForm.Add_KeyDown({if($_.KeyCode -eq "Escape") {
        $objForm.Close()}})
    $objForm.Add_KeyDown({if ($_.KeyCode -eq "Enter") {
        if ($objTextBox.Text -eq $null -or $objTextBox.Text.Equals("")){
            $objTextBox.AppendText("null")}
        $objForm.Close()}})

    $objLabel = New-Object System.Windows.Forms.Label
    $objLabel.Location = New-Object System.Drawing.Size(5,20) 
    $objLabel.Size = New-Object System.Drawing.Size(320,30) 
    $objLabel.Text = "$prompt"

    $objForm.Controls.Add($objLabel) 

    $objTextBox = New-Object System.Windows.Forms.TextBox 
    $objTextBox.Location = New-Object System.Drawing.Size(10,50) 
    $objTextBox.Size = New-Object System.Drawing.Size(260,20) 
    if (!$button2) {$objForm.Controls.Add($objTextBox)}
    if ($button2){if ($button2.Equals("Cancel")){$objForm.Controls.Add($objTextBox)}}    
    $OKButton = New-Object System.Windows.Forms.Button
    $OKButton.Location = New-Object System.Drawing.Size(10,75)
    $OKButton.Size = New-Object System.Drawing.Size(75,23)
    $OKButton.Text = "$button1"
    $OKButton.Add_Click({
        if ($objTextBox.Text -eq $null -or $objTextBox.Text.Equals("")){
            $objTextBox.AppendText("null")}
        $objForm.Close()})

    $CancelButton = New-Object System.Windows.Forms.Button
    $CancelButton.Location = New-Object System.Drawing.Size(100,75)
    $CancelButton.Size = New-Object System.Drawing.Size(75,23)
    $CancelButton.Text = "$button2"
    $CancelButton.Add_Click({$objForm.Close()})

    $objForm.Controls.Add($OKButton)
    if ($button2) {$objForm.Controls.Add($CancelButton)}
    $objForm.Topmost = $True
    $objForm.Add_Shown({$objForm.Activate()})
    [void] $objForm.ShowDialog()

    return $objTextBox.Text
}

Function Browse-AD(){
    # original inspiration: https://itmicah.wordpress.com/2013/10/29/active-directory-ou-picker-in-powershell/
    # author: Rene Horn the.rhorn@gmail.com
<#
    Copyright (c) 2015, Rene Horn
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#>
    $dc_hash = @{}
    $selected_ou = $null

    $forest = Get-ADForest
    [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing") | Out-Null
    [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") | Out-Null

    function Get-NodeInfo($sender, $dn_textbox) {
        $selected_node = $sender.Node
        $dn_textbox.Text = $selected_node.Name
    }

    function Add-ChildNodes($sender) {
        $expanded_node = $sender.Node

        if ($expanded_node.Name -eq "root") {
            return
        }

        $expanded_node.Nodes.Clear() | Out-Null

        $dc_hostname = $dc_hash[$($expanded_node.Name -replace '(OU=[^,]+,)*((DC=\w+,?)+)','$2')]
        $child_OUs = Get-ADObject -Server $dc_hostname -Filter 'ObjectClass -eq "organizationalUnit" -or ObjectClass -eq "container"' -SearchScope OneLevel -SearchBase $expanded_node.Name
        if($child_OUs -eq $null) {
            $sender.Cancel = $true
        } else {
            foreach($ou in $child_OUs) {
                $ou_node = New-Object Windows.Forms.TreeNode
                $ou_node.Text = $ou.Name
                $ou_node.Name = $ou.DistinguishedName
                $ou_node.Nodes.Add('') | Out-Null
                $expanded_node.Nodes.Add($ou_node) | Out-Null
            }
        }
    }

    function Add-ForestNodes($forest, [ref]$dc_hash){
        $ad_root_node = New-Object Windows.Forms.TreeNode
        $ad_root_node.Text = $forest.RootDomain
        $ad_root_node.Name = "root"
        $ad_root_node.Expand()

        $i = 1
        foreach ($ad_domain in $forest.Domains) {
            Write-Progress -Activity "Querying AD forest for domains and hostnames..." -Status $ad_domain -PercentComplete ($i++ / $forest.Domains.Count * 100)
            $dc = Get-ADDomainController -Server $ad_domain
            $dn = $dc.DefaultPartition
            $dc_hash.Value.Add($dn, $dc.Hostname)
            $dc_node = New-Object Windows.Forms.TreeNode
            $dc_node.Name = $dn
            $dc_node.Text = $dc.Domain
            $dc_node.Nodes.Add("") | Out-Null
            $ad_root_node.Nodes.Add($dc_node) | Out-Null
        }
        return $ad_root_node
    }
    
    $main_dlg_box = New-Object System.Windows.Forms.Form
    $main_dlg_box.ClientSize = New-Object System.Drawing.Size(400,600)
    $main_dlg_box.Text = "Create Users: AD Browser"
    $main_dlg_box.ShowIcon = $False
    $main_dlg_box.MaximizeBox = $false
    $main_dlg_box.MinimizeBox = $false
    $main_dlg_box.FormBorderStyle = 'FixedSingle'

    $objLabel = New-Object System.Windows.Forms.Label
    $objLabel.Location = New-Object System.Drawing.Size(10,20) 
    $objLabel.Size = New-Object System.Drawing.Size(280,20) 
    $objLabel.Text = "Choose a location for the New Users:"
    $main_dlg_box.Controls.Add($objLabel) 

    # widget size and location variables
    $ctrl_width_col = $main_dlg_box.ClientSize.Width/20
    $ctrl_height_row = $main_dlg_box.ClientSize.Height/15
    $max_ctrl_width = $main_dlg_box.ClientSize.Width - $ctrl_width_col*2
    $max_ctrl_height = $main_dlg_box.ClientSize.Height - $ctrl_height_row
    $right_edge_x = $max_ctrl_width
    $left_edge_x = $ctrl_width_col
    $bottom_edge_y = $max_ctrl_height
    $top_edge_y = $ctrl_height_row

    # setup text box showing the distinguished name of the currently selected node
    $dn_text_box = New-Object System.Windows.Forms.TextBox
    # can not set the height for a single line text box, that's controlled by the font being used
    $dn_text_box.Width = (14 * $ctrl_width_col)
    $dn_text_box.Location = New-Object System.Drawing.Point($left_edge_x, ($bottom_edge_y - $dn_text_box.Height))
    $main_dlg_box.Controls.Add($dn_text_box)
    # /text box for dN

    # setup Ok button
    $ok_button = New-Object System.Windows.Forms.Button
    $ok_button.Size = New-Object System.Drawing.Size(($ctrl_width_col * 2), $dn_text_box.Height)
    $ok_button.Location = New-Object System.Drawing.Point(($right_edge_x - $ok_button.Width), ($bottom_edge_y - $ok_button.Height))
    $ok_button.Text = "Ok"
    $ok_button.DialogResult = 'OK'
    $main_dlg_box.Controls.Add($ok_button)  
    # /Ok button

    # New OU Button
    $new_ou = New-Object System.Windows.Forms.Button
    $new_ou.Size = New-Object System.Drawing.Size(($ctrl_width_col * 7), $dn_text_box.Height)
    $new_ou.Location = New-Object System.Drawing.Point(($left_edge_x), ($bottom_edge_y + 10))
    $new_ou.Text = "New Organizational Unit"
    $new_ou.Add_Click({
        $ou_root_path = $dn_text_box.Text;
        if($ou_root_path.Equals("root") -or $ou_root_path.Equals("")){
            [System.Windows.Forms.MessageBox]::Show("A new Organizational Utit cannot be created inside `"root`"")|Out-Null
        } else {
            $valid_ou_path = $False
            While(!$valid_ou_path){
                $ou_name = Custom-Dialog "Create Users: New OU" "Name of Organizational Unit to create inside $ou_root_path" "OK" "Cancel"
                if ($ou_name.Equals("null")){
                    [System.Windows.Forms.MessageBox]::Show("`"$ou_name`" is not a valid OU name")|Out-Null
                } elseif ($ou_name -match "^OU=."){
                    [System.Windows.Forms.MessageBox]::Show("The `"OU=`" prefix should not be included")|Out-Null
                } else {
                    $valid_ou_path = $True
                }
            }
            $ou_path = "OU=$ou_name,$ou_root_path"
            New-ADOrganizationalUnit -Name $ou_name -Path $ou_root_path
            Write-Host "New OU path: $ou_path"
            $dn_text_box.Clear()
            $dn_text_box.AppendText("refresh")
            $main_dlg_box.Close()
        }

    })
    $main_dlg_box.Controls.Add($new_ou)

    # setup tree selector showing the domains
    $ad_tree_view = New-Object System.Windows.Forms.TreeView
    $ad_tree_view.Size = New-Object System.Drawing.Size($max_ctrl_width, ($max_ctrl_height - $dn_text_box.Height - $ctrl_height_row*1.5))
    $ad_tree_view.Location = New-Object System.Drawing.Point($left_edge_x, $top_edge_y)
    $ad_tree_view.Nodes.Add($(Add-ForestNodes $forest ([ref]$dc_hash))) | Out-Null
    $ad_tree_view.Add_BeforeExpand({Add-ChildNodes $_})
    $ad_tree_view.Add_AfterSelect({Get-NodeInfo $_ $dn_text_box})
    $main_dlg_box.Controls.Add($ad_tree_view)
    # /tree selector

    $main_dlg_box.ShowDialog() | Out-Null
    return  $dn_text_box.Text
}

# Collect information
$realm = [System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest().Name.ToString()
$realm = $realm.ToUpper()

# Find a place in Active directory
$path = ""
$valid_path = $False
While (!$valid_path){
    $path = Browse-AD
    if($path.Equals("")){Exit}
    if ($path.Equals("root") -or $path -notmatch "^OU="){
        if (!$path.Equals("refresh")){
            [System.Windows.Forms.MessageBox]::Show("`"$path`" is not a valid Organizational Unit")
        }
    } else {$valid_path = $True}
}
Write-Host "Using the path `"$path`""

# Obtain number of users to create
$is_digit = $False
while (!$is_digit){
    $number = Custom-Dialog "Create Users: Number of users" "Number of users to create:" "OK"
    if($number.Equals("")){Exit}
    if($number -match "\d+" -and $number -notmatch "^0"){$is_digit = $True}
    else {[System.Windows.Forms.MessageBox]::Show("`"$number`" is not a valid integer")|Out-Null}
}

# Obtain Starting number
$is_digit = $False
while (!$is_digit){
    $start = Custom-Dialog "Create Users: Start Count" "Starting counting at [0]:" "OK"
        if($start.Equals("")){Exit}
    if($start.Equals("null")){$start = "0"}
    if($start -match "\d+"){$is_digit = $True}
    else {[System.Windows.Forms.MessageBox]::Show("`"$start`" is not a valid integer")|Out-Null}
}

# Obtain Base name
$is_null = $True
while ($is_null){
    $base_name = Custom-Dialog "Create Users: Base name" "Base user name:" "OK"
    if ($base_name.Equals("")){Exit}
    if($base_name.Equals("null") -or $base_name -match "^\d+" -or $base_name -match ".\s."){
        [System.Windows.Forms.MessageBox]::Show("`"$base_name`" is not a valid base name")|Out-Null
    }
    else {$is_null = $False}
}

# Obtain e-mail domain
$valid_email = $False
while(!$valid_email){
    $email = Custom-Dialog "Create Users: Set E-mail" "E-Mail Address Domain: `n$base_name$end@" "OK" "Cancel"
    if ($email.Equals("null") -or $email.Equals("")){$email = $realm.ToLower()}
    if($email -match "^\d+" -or $email -match ".\s." -or $email -match ".@." -or $email -notmatch ".+\.+"){
        [System.Windows.Forms.MessageBox]::Show("`"$email`" is not a valid E-mail Domain")|Out-Null
    } else {$valid_email = $True}
} 

# Set password
$valid_password = $False
while(!$valid_password){
    $password = Custom-Dialog "Create Users: Set Password" "Password for test users:" "OK" "Cancel"
    if($password -match ".\s."){
        [System.Windows.Forms.MessageBox]::Show("`"$password`" is not a password")|Out-Null
    } else {$valid_password = $True}
} 

# Verify Action
$end = [convert]::ToInt32($start) + [convert]::ToInt32($number) - 1
$response = Custom-Dialog "Create Users" "Usernames: $base_name<$start - $end>@$email `nPath: $path" "Continue" "Abort"
# If "Cancel" was clicked or "Escape" was pressed
if (!$response.Equals("null")){Exit}

# Create AD Users
for ($i = [convert]::ToInt32($start); $i -le $end; $i++){
    # Show the same number of digits as the largest number in the series
    $digits = $end.ToString().Length 
    $user_name = $base_name + ("{0:D$digits}" -f $i).ToString()
    Write-Progress -Activity "Creating user in $path" -Status "$user_name@($realm|$email) $surname" `
        -PercentComplete(($i - [convert]::ToInt32($start))/($end - [convert]::ToInt32($start))*100)
    try {
        New-ADUser -Name $user_name -SamAccountName $user_name -DisplayName $user_name -GivenName $user_name -Surname $base_name.ToUpper()`
            -AccountPassword (ConvertTo-SecureString "$password" -AsPlainText -force) -PasswordNeverExpires $True `
            -UserPrincipalName "$user_name@$realm" -Email "$user_name@$email" -Path "$path" -Description "Test User" -Enabled $True
    } catch {
        Write-Host "$user_name already exists"
    }

}

# End script
[System.Windows.Forms.MessageBox]::Show("Finished!`n$number users created in $path")|Out-Null
