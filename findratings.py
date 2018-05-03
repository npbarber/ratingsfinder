#!/usr/bin/env python

import argparse


def read_file(filename):
    result = {}
    f = open(filename, 'r')
    with f:
        for line in f:
            parts = line.split('","')
            ayso_id = parts[23]
            rating = parts[26]
            first_name = parts[4]
            last_name = parts[5]
            result[ayso_id] = {
                'rating': rating,
                'fname': first_name,
                'lname': last_name,
            }
    return result


def find_players_missing_rating(left, right):
    result = []
    for ayso_id, details in left.items():
        # skip this entry is there is no rating in the left data
        if not details['rating']:
            continue

        # grab the rating from the right. If the ayso id does not
        # exist on the right side, skip it.
        try:
            right_rating = right[ayso_id]['rating']
        except KeyError:
            continue

        # skip this entry if we already have a rating in the right data
        if right_rating:
            continue

        result.append(
            (ayso_id, details['fname'], details['lname'], details['rating']))

    # sort by player last name
    result = sorted(result, key=lambda x: x[2].lower())
    return result


def output(data):
    for line in data:
        print('%s\t%s\t%s\t%s' % line)


def parse_args():
    parser = argparse.ArgumentParser(
        description='find missing ratings from prior program')
    parser.add_argument(
        '--left', required=True, help='enrollment report from a prior season')
    parser.add_argument(
        '--right',
        required=True,
        help='enrollment report from a current season')
    return parser.parse_args()


def main(args):
    left = read_file(args.left)
    right = read_file(args.right)
    found_ratings = find_players_missing_rating(left, right)
    output(found_ratings)


if __name__ == '__main__':
    args = parse_args()
    main(args)
