#!/usr/bin/env python3
"""SQLite 資料庫操作範例 — 圖書館管理系統"""

import sqlite3

DB_PATH = "library.db"


def create_tables(conn):
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birth_year INTEGER
        );

        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            published_year INTEGER,
            isbn TEXT UNIQUE,
            FOREIGN KEY (author_id) REFERENCES authors(id)
        );

        CREATE TABLE IF NOT EXISTS readers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            reader_id INTEGER NOT NULL,
            loan_date DATE NOT NULL,
            due_date DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (reader_id) REFERENCES readers(id)
        );
    """)
    conn.commit()


def insert_sample_data(conn):
    cursor = conn.cursor()

    authors = [
        (1, '陳鍾誠', 1965),
        (2, '張三', 1980),
        (3, '李四', 1975),
        (4, '王五', 1990),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO authors (id, name, birth_year) VALUES (?, ?, ?)",
        authors,
    )

    books = [
        (1, '資料庫系統概論', 1, 2024, '978-986-111-111-1'),
        (2, 'SQL 實戰寶典', 2, 2025, '978-986-222-222-2'),
        (3, 'Python 程式設計', 3, 2023, '978-986-333-333-3'),
        (4, '資料結構與演算法', 4, 2024, '978-986-444-444-4'),
        (5, '深度學習入門', 1, 2025, '978-986-555-555-5'),
        (6, '作業系統概念', 3, 2022, '978-986-666-666-6'),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO books (id, title, author_id, published_year, isbn) VALUES (?, ?, ?, ?, ?)",
        books,
    )

    readers = [
        (1, '王小明', 'wang@test.com'),
        (2, '李小華', 'lee@test.com'),
        (3, '張小英', 'chang@test.com'),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO readers (id, name, email) VALUES (?, ?, ?)",
        readers,
    )

    loans = [
        (1, 1, 1, '2026-06-01', '2026-06-15', None),
        (2, 2, 1, '2026-06-05', '2026-06-19', None),
        (3, 3, 2, '2026-06-10', '2026-06-24', '2026-06-22'),
        (4, 5, 3, '2026-06-15', '2026-06-29', None),
        (5, 4, 1, '2026-06-20', '2026-07-04', None),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO loans (id, book_id, reader_id, loan_date, due_date, return_date) VALUES (?, ?, ?, ?, ?, ?)",
        loans,
    )

    conn.commit()


def demo():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    create_tables(conn)
    insert_sample_data(conn)

    cursor = conn.cursor()

    print("=== 基本查詢：所有書籍 ===")
    cursor.execute("SELECT id, title, published_year FROM books ORDER BY published_year DESC")
    for row in cursor.fetchall():
        print(f"  {row['title']} ({row['published_year']})")

    print("\n=== JOIN 查詢：書籍與作者 ===")
    cursor.execute("""
        SELECT b.title, a.name AS author, b.published_year
        FROM books b
        INNER JOIN authors a ON b.author_id = a.id
        ORDER BY a.name, b.published_year
    """)
    for row in cursor.fetchall():
        print(f"  《{row['title']}》— {row['author']} ({row['published_year']})")

    print("\n=== 聚合查詢：每位讀者借閱統計 ===")
    cursor.execute("""
        SELECT r.name AS reader,
               COUNT(l.id) AS loan_count,
               COUNT(l.return_date) AS returned_count
        FROM readers r
        LEFT JOIN loans l ON r.id = l.reader_id
        GROUP BY r.id
        ORDER BY loan_count DESC
    """)
    for row in cursor.fetchall():
        print(f"  {row['reader']}: {row['loan_count']} 次借閱，已還 {row['returned_count']} 本")

    print("\n=== 子查詢：目前借出的書籍 ===")
    cursor.execute("""
        SELECT b.title, r.name AS reader, l.loan_date, l.due_date
        FROM loans l
        INNER JOIN books b ON l.book_id = b.id
        INNER JOIN readers r ON l.reader_id = r.id
        WHERE l.return_date IS NULL
    """)
    for row in cursor.fetchall():
        print(f"  《{row['title']}》借給 {row['reader']}，到期日 {row['due_date']}")

    print("\n=== 進階查詢：每位作者被借閱次數 ===")
    cursor.execute("""
        SELECT a.name, COUNT(l.id) AS total_loans
        FROM authors a
        LEFT JOIN books b ON a.id = b.author_id
        LEFT JOIN loans l ON b.id = l.book_id
        GROUP BY a.id
        ORDER BY total_loans DESC
    """)
    for row in cursor.fetchall():
        print(f"  {row['name']}: {row['total_loans']} 次")

    print("\n=== 交易範例：借書操作 ===")
    try:
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute(
            "INSERT INTO loans (book_id, reader_id, loan_date, due_date) VALUES (?, ?, DATE('now'), DATE('now', '+14 days'))",
            (6, 3),
        )
        print("  借書成功：張小英借了《作業系統概念》")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"  借書失敗：{e}")

    conn.close()
    print("\n所有範例執行完畢！")


if __name__ == "__main__":
    demo()
