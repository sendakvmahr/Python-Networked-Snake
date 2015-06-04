<h1>
    Highscores
</h1>

<?php
    $db = new SQLite3('./server/users.db');
    $tablesquery = $db->query("SELECT name, win, game FROM user");

    while ($table = $tablesquery->fetchArray(SQLITE3_ASSOC)) {
        $win;
        if ( $table['game'] == 0) {
            $win = 0;
        }
        else {
            $win = $table['win'] / $table['game'];
        }
        $win = number_format ($win, 2);
        echo "name: " . $table['name'] . "<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Win Ratio: " . $win . '<br/><br/>';
    }
?>
