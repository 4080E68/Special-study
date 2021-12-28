<?php
$db_host = "localhost";
$db_name = "1228";
$db_table = "func3api_display";
$db_user = "root";
$db_password = "";
// check connection
$dept = str_replace("'", "''", $_REQUEST['dept']); //抓取前端資料

$conn = mysqli_connect($db_host, $db_user, $db_password);
if (empty($conn)) {
   
    die("Unable to connect to DB！");
    exit;
}
if (!mysqli_select_db($conn, $db_name)) {
    die("DB is not existed");
    exit;
}

mysqli_set_charset($conn, 'utf8');

echo "ksu_std_table: the number of students as follows:" . "<br/><br/>";

$sql = "SELECT id,name,price FROM `func3api_display` WHERE like '%$dept%'";

$result = mysqli_query($conn, $sql);
//$num = mysqli_num_rows($result);//計算取得資料的筆數
echo "<table border='1'>
 <tr>
    <th> Name </th> <th> Grade </th> <th> Memo </th> 
 </tr>";

$row_num = 0;
while ($row = mysqli_fetch_array($result)) {
    if (empty($row['id']) != true) {
        echo "<tr>";
        echo "<td>" . $row['id'] . "</td>";
        echo "<td >" . $row['name'] . "</td>";
        echo "<td >" . $row['price'] . "</td>";
        echo "</tr>";
        $row_num += 1;
    }
}

echo "</table>";
echo $row_num . " records found!" . "<br/>";

?>
<form enctype="multipart/form-data" method="post" action="ksu_select3en-bug_copy.html">
    <input type="submit" name="sub" value="Back" />
</form>