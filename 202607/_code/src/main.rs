use anyhow::{Context, Result};
use clap::Parser;
use regex::Regex;
use std::fs;
use std::io::{BufRead, BufReader};
use std::path::PathBuf;

/// Mini-grep: a simple pattern search tool
#[derive(Parser, Debug)]
#[command(name = "mini-grep", version, about = "Search for patterns in files")]
struct Args {
    /// Pattern to search for (regex supported)
    pattern: String,

    /// File path to search in (use - for stdin)
    path: PathBuf,

    /// Case-insensitive search
    #[arg(short, long)]
    ignore_case: bool,

    /// Show line numbers
    #[arg(short = 'n', long)]
    line_number: bool,

    /// Invert match (show non-matching lines)
    #[arg(short = 'v', long)]
    invert: bool,

    /// Maximum count of matching lines to show
    #[arg(short = 'm', long)]
    max_count: Option<usize>,
}

struct SearchResult {
    line_number: usize,
    line: String,
    is_match: bool,
}

fn search_in_reader<R: BufRead>(
    reader: R,
    re: &Regex,
    args: &Args,
) -> Vec<SearchResult> {
    reader
        .lines()
        .enumerate()
        .filter_map(|(idx, line)| {
            let line = line.ok()?;
            let line_number = idx + 1;
            let is_match = re.is_match(&line);
            Some(SearchResult { line_number, line, is_match })
        })
        .filter(|r| if args.invert { !r.is_match } else { r.is_match })
        .take(args.max_count.unwrap_or(usize::MAX))
        .collect()
}

fn print_results(results: &[SearchResult], path: &PathBuf, args: &Args) {
    if results.is_empty() {
        return;
    }

    let show_filename = true;
    for r in results {
        if show_filename {
            if args.line_number {
                println!(
                    "{}:{}:{}",
                    path.display(),
                    r.line_number,
                    r.line
                );
            } else {
                println!("{}:{}", path.display(), r.line);
            }
        } else if args.line_number {
            println!("{}:{}", r.line_number, r.line);
        } else {
            println!("{}", r.line);
        }
    }
}

fn run(args: &Args) -> Result<()> {
    let pattern = if args.ignore_case {
        format!("(?i){}", args.pattern)
    } else {
        args.pattern.clone()
    };

    let re = Regex::new(&pattern)
        .with_context(|| format!("Invalid regex pattern: '{}'", args.pattern))?;

    let content = fs::read_to_string(&args.path)
        .with_context(|| format!("Could not read file '{}'", args.path.display()))?;

    let results = search_in_reader(
        BufReader::new(content.as_bytes()),
        &re,
        args,
    );

    print_results(&results, &args.path, args);

    if results.is_empty() {
        eprintln!("No matches found for pattern '{}' in '{}'", args.pattern, args.path.display());
    }

    Ok(())
}

fn main() -> Result<()> {
    let args = Args::parse();
    run(&args)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Cursor;

    #[test]
    fn test_basic_search() {
        let content = "hello world\nfoo bar\nhello rust\n";
        let re = Regex::new("hello").unwrap();
        let args = Args {
            pattern: "hello".to_string(),
            path: PathBuf::from("test.txt"),
            ignore_case: false,
            line_number: false,
            invert: false,
            max_count: None,
        };

        let results = search_in_reader(
            BufReader::new(Cursor::new(content)),
            &re,
            &args,
        );
        assert_eq!(results.len(), 2);
        assert!(results[0].line.contains("hello world"));
        assert!(results[1].line.contains("hello rust"));
    }

    #[test]
    fn test_case_insensitive() {
        let content = "Hello World\nfoo bar\nHELLO RUST\n";
        let re = Regex::new("(?i)hello").unwrap();
        let args = Args {
            pattern: "hello".to_string(),
            path: PathBuf::from("test.txt"),
            ignore_case: true,
            line_number: false,
            invert: false,
            max_count: None,
        };

        let results = search_in_reader(
            BufReader::new(Cursor::new(content)),
            &re,
            &args,
        );
        assert_eq!(results.len(), 2);
    }

    #[test]
    fn test_invert_match() {
        let content = "hello world\nfoo bar\nhello rust\n";
        let re = Regex::new("hello").unwrap();
        let args = Args {
            pattern: "hello".to_string(),
            path: PathBuf::from("test.txt"),
            ignore_case: false,
            line_number: false,
            invert: true,
            max_count: None,
        };

        let results = search_in_reader(
            BufReader::new(Cursor::new(content)),
            &re,
            &args,
        );
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].line, "foo bar");
    }

    #[test]
    fn test_line_numbers() {
        let content = "hello world\nfoo bar\nhello rust\n";
        let re = Regex::new("hello").unwrap();
        let args = Args {
            pattern: "hello".to_string(),
            path: PathBuf::from("test.txt"),
            ignore_case: false,
            line_number: true,
            invert: false,
            max_count: None,
        };

        let results = search_in_reader(
            BufReader::new(Cursor::new(content)),
            &re,
            &args,
        );
        assert_eq!(results[0].line_number, 1);
        assert_eq!(results[1].line_number, 3);
    }

    #[test]
    fn test_max_count() {
        let content = "hello world\nfoo bar\nhello rust\nhello again\n";
        let re = Regex::new("hello").unwrap();
        let args = Args {
            pattern: "hello".to_string(),
            path: PathBuf::from("test.txt"),
            ignore_case: false,
            line_number: false,
            invert: false,
            max_count: Some(2),
        };

        let results = search_in_reader(
            BufReader::new(Cursor::new(content)),
            &re,
            &args,
        );
        assert_eq!(results.len(), 2);
    }

    #[test]
    fn test_regex_pattern() {
        let content = "apple\nbanana\ncherry\napricot\n";
        let re = Regex::new("^a").unwrap();
        let args = Args {
            pattern: "^a".to_string(),
            path: PathBuf::from("test.txt"),
            ignore_case: false,
            line_number: false,
            invert: false,
            max_count: None,
        };

        let results = search_in_reader(
            BufReader::new(Cursor::new(content)),
            &re,
            &args,
        );
        assert_eq!(results.len(), 2);
        assert_eq!(results[0].line, "apple");
        assert_eq!(results[1].line, "apricot");
    }
}
