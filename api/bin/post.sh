#!/bin/sh

http --verbose POST localhost:8080/users/ @"$1"