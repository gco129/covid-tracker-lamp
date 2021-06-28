<html>
	<head>
		<title>COVID-19 Tracker</title>
	</head>
	<body>
		<p><center><font size="+3">COVID-19 Tracker - United States</font></center></p>
		<table>
		<?php
			// Establish connection to MySQL
			$server = "localhost";
			$user = "root";
			$pass = "mypassword";
			$db = "us_covid_cases";
			$connection = new mysqli($server, $user, $pass, $db);
			
			// Get order and column to sort by
			$col = "cases";
			$order = "DESC";
			
			if($_GET["order"] == "DESC"){
				$order = "ASC";
			}
			else{
				$order = "DESC";
			}
			
			if($_GET["col"] == "state"){
				$col = "state";
			}
			else if($_GET["col"] == "cases"){
				$col = "cases";
			}
			else if($_GET["col"]== "newcases"){
				$col = "oldcases";
			}
			else if($_GET["col"]== "deaths"){
				$col = "deaths";
			}
			else if($_GET["col"]== "newdeaths"){
				$col = "olddeaths";
			}
			
			// Display table in order of amount of cases, descending
			$sqlcmd = "SELECT * FROM us ORDER BY $col $order;";
			$result = $connection->query($sqlcmd);
			
			// Set up headers to change order upon click, display table in the page properly
		?>
		<tr>
			<th><a href="covidsite.php?order=<?php echo $order; ?>&col=state">States</a></th>
			<th><a href="covidsite.php?order=<?php echo $order; ?>&col=cases">Confirmed Cases</a></th>
			<th><a href="covidsite.php?order=<?php echo $order; ?>&col=newcases">New Cases</a></th>
			<th><a href="covidsite.php?order=<?php echo $order; ?>&col=deaths">Confirmed Deaths</a></th>
			<th><a href="covidsite.php?order=<?php echo $order; ?>&col=newdeaths">New Deaths</a></th>
		</tr>
		<tbody>
			<?php
				// Run parser to update database with new cases
				$cmd = escapeshellcmd('parser.py');
				$output = shell_exec($cmd);
				echo $output;
			?>
			<tr>
				<?php while($row = $result->fetch_assoc()){ ?>
				<td><?php echo $row['state']; ?></td>
				<td><?php echo $row['cases']; ?></td>
				<td><?php echo $row['cases'] - $row['oldcases']; ?></td>
				<td><?php echo $row['deaths']; ?></td>
				<td><?php echo $row['deaths'] - $row['olddeaths']; ?></td>
			</tr>
		<?php } ?>
		</tbody>
		</table>
	</body>
</html>