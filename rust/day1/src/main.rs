use std::{collections::HashMap, fs};

fn parse_input() -> (Vec<i32>, Vec<i32>) {
    let mut first_list: Vec<i32> = Vec::new();
    let mut second_list: Vec<i32> = Vec::new();
    let problem_input =
        fs::read_to_string("day1.txt").expect("day1.txt should be at the root of this project");
    for line in problem_input.lines() {
        let line_numbers: Vec<i32> = line
            .trim()
            .split_whitespace()
            .map(|s| s.parse::<i32>().expect("Should be an integer"))
            .collect();
        if let [first, second] = line_numbers[..] {
            first_list.push(first);
            second_list.push(second);
        } else {
            panic!("Invalid format for line, should be only two numbers");
        }
    }

    if first_list.len() != second_list.len() {
        panic!("Lists are not the same length");
    }

    first_list.sort();
    second_list.sort();

    (first_list, second_list)
}

fn part_one(first_list: &Vec<i32>, second_list: &Vec<i32>) -> i32 {
    let mut index = 0;
    let mut distance = 0;

    while index < first_list.len() && index < second_list.len() {
        let dist_one = first_list[index];
        let dist_two = second_list[index];
        distance += (dist_two - dist_one).abs();
        index += 1;
    }

    distance
}

fn part_two(first_list: &Vec<i32>, second_list: &Vec<i32>) -> i32 {
    let mut similarity_score: i32 = 0;
    let mut list_two_counts: HashMap<i32, i32> = HashMap::new();
    for num in second_list {
        list_two_counts
            .entry(*num)
            .and_modify(|count| *count += 1)
            .or_insert(1);
    }

    for dist in first_list {
        if let Some(two_dist) = list_two_counts.get(dist) {
            similarity_score += *dist * two_dist;
        }
    }

    similarity_score
}

fn main() {
    let (first_list, second_list) = parse_input();
    println!("Part One: {}", part_one(&first_list, &second_list));
    println!("Part Two: {}", part_two(&first_list, &second_list));
}
