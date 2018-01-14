<?php
if ($_POST) {
  $index = $_POST["first_index"];
} else {
  $index = 0;
}
?>
<!DOCTYPE html>
<html>
<style>
  .canvas {
    border: 1px solid black;
  }
</style>
<body>
<script>
  function change(){
    document.getElementById("index_select").submit();
  }
</script>
<form id="index_select" method="post">
  <select name="first_index" onchange="change()">
  <?php
    $file_count = 3214;
    for ($i=0; $i<floor($file_count/10); $i++) {
      $begin = $i*10;
      $end = ($i*10)+9;
      echo "<option value='$begin'>$begin-$end</option>";
    } 
  ?>
  </select>
</form>
<hr>
<iframe class="canvas" height="350px" width="350px" src="d3.php?filename=data/dhry_sg/<?php echo ($index+0);?>"></iframe>
<iframe class="canvas" height="350px" width="350px" src="d3.php?filename=data/dhry_sg/<?php echo ($index+1);?>"></iframe>
<iframe class="canvas" height="350px" width="350px" src="d3.php?filename=data/dhry_sg/<?php echo ($index+2);?>"></iframe>
<iframe class="canvas" height="350px" width="350px" src="d3.php?filename=data/dhry_sg/<?php echo ($index+3);?>"></iframe>
<iframe class="canvas" height="350px" width="350px" src="d3.php?filename=data/dhry_sg/<?php echo ($index+4);?>"></iframe>
<iframe class="canvas" height="350px" width="350px" src="d3.php?filename=data/dhry_sg/<?php echo ($index+5);?>"></iframe>
<iframe class="canvas" height="350px" width="350px" src="d3.php?filename=data/dhry_sg/<?php echo ($index+6);?>"></iframe>
<iframe class="canvas" height="350px" width="350px" src="d3.php?filename=data/dhry_sg/<?php echo ($index+7);?>"></iframe>
<iframe class="canvas" height="350px" width="350px" src="d3.php?filename=data/dhry_sg/<?php echo ($index+8);?>"></iframe>
<iframe class="canvas" height="350px" width="350px" src="d3.php?filename=data/dhry_sg/<?php echo ($index+9);?>"></iframe>

</body>
</html>

