#!/usr/bin/perl -w

use DBI;
use CGI qw(:standard);
print header;

our %config;
do '/openils/conf/live-db-setup.pl';

my $bcode = param('bcode');

unless ($bcode) {
  print "<form method=post>Enter Item Barcode: <input name=bcode><submit></form><p>";
  exit;
}

my $dbh = DBI->connect($config{dsn},$config{usr},$config{pw});
my $cid = $dbh->prepare("select id,location from asset.copy where barcode=?");
$cid->execute($bcode);
my $cr = $cid->fetch;
my $cp = $cr->[0];
my $cl = $cr->[1];

my $odresult = `/usr/local/pgsql/bin/psql -U postgres -c "select * from smart_float.opens_and_dups('$bcode')" -H evergreen`;
print "Item $bcode Location $cl <br> $odresult";

foreach $cklib (11..17){
print "Checkin at $cklib<br>";
$dresult = `/usr/local/pgsql/bin/psql -U postgres -c "select * from smart_float.destination($cklib,$cp)" -H evergreen`;
print $dresult;
print "Metrics<br>";
$mresult = `/usr/local/pgsql/bin/psql -U postgres -c "select * from smart_float.metrics where copy_id = $cp order by id desc limit 2" -H evergreen`;
print $mresult;
}

exit;
