#!/usr/bin/perl
use strict;
use warnings;
use Text::CSV;

my $file = $ARGV[0] or die "Need to get CSV file on the command line\n";

my $csv = Text::CSV->new ({
  binary    => 1,
  auto_diag => 1,
  sep_char  => ','    # not really needed as this is the default
});

open(my $data, '<:encoding(utf8)', $file) or die "Could not open '$file' $!\n";

print "Monitor Title,Monitor Type,Parameters\n";

while (my $fields = $csv->getline( $data ))
{
my $f0 = $fields->[0];
my $f1 = $fields->[1];
my $f6 = $fields->[6];
if ($f1 eq "Database Query")
{
my @m = ($f6 =~ m/^(?:\S+\s+){3}(\S+)</g);
print "$f0,$f1,@m\n";
}
}
if (not $csv->eof)
{
  $csv->error_diag();
}
close $data;
 
