#!/usr/bin/perl

while(<STDIN>)
{
    next if !/0x/;
    s/0x//g;
    s/[^0-9a-f]//g;
    print $_;
}
