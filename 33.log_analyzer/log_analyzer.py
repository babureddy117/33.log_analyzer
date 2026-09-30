import re
from collections import Counter, defaultdict
from datetime import datetime

class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logs = []
        self.load_logs()

    def load_logs(self):
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    parsed = self.parse_log(line.strip())
                    if parsed:
                        self.logs.append(parsed)
            print(f"Loaded {len(self.logs)} log entries\n")
        except FileNotFoundError:
            print(f"Error: {self.log_file} not found")

    def parse_log(self, line):
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (\w+) - (.+)'
        match = re.match(pattern, line)
        if match:
            return {
                'timestamp': match.group(1),
                'level': match.group(2),
                'message': match.group(3)
            }
        return None

    def filter_by_level(self, level):
        filtered = [log for log in self.logs if log['level'] == level.upper()]
        print(f"\n=== {level.upper()} Logs ({len(filtered)}) ===")
        for log in filtered:
            print(f"{log['timestamp']} - {log['message']}")

    def count_by_level(self):
        levels = Counter(log['level'] for log in self.logs)
        print("\n=== Log Level Summary ===")
        for level, count in levels.most_common():
            print(f"{level}: {count}")

    def search(self, keyword):
        results = [log for log in self.logs if keyword.lower() in log['message'].lower()]
        print(f"\n=== Search Results for '{keyword}' ({len(results)}) ===")
        for log in results:
            print(f"{log['timestamp']} - {log['level']} - {log['message']}")

    def errors_summary(self):
        errors = [log for log in self.logs if log['level'] in ['ERROR', 'CRITICAL']]
        print(f"\n=== Errors & Critical Issues ({len(errors)}) ===")
        for log in errors:
            print(f"{log['timestamp']} - {log['level']} - {log['message']}")

    def time_range(self, start_time, end_time):
        filtered = []
        for log in self.logs:
            log_time = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S')
            start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            if start <= log_time <= end:
                filtered.append(log)
        
        print(f"\n=== Logs from {start_time} to {end_time} ({len(filtered)}) ===")
        for log in filtered:
            print(f"{log['timestamp']} - {log['level']} - {log['message']}")

    def top_messages(self, n=5):
        messages = Counter(log['message'] for log in self.logs)
        print(f"\n=== Top {n} Most Frequent Messages ===")
        for message, count in messages.most_common(n):
            print(f"{count}x - {message}")

    def hourly_distribution(self):
        hours = defaultdict(int)
        for log in self.logs:
            hour = log['timestamp'].split()[1].split(':')[0]
            hours[hour] += 1
        
        print("\n=== Hourly Log Distribution ===")
        for hour in sorted(hours.keys()):
            bar = '█' * (hours[hour] // 2)
            print(f"{hour}:00 - {hours[hour]:3d} {bar}")

    def statistics(self):
        total = len(self.logs)
        levels = Counter(log['level'] for log in self.logs)
        
        print("\n=== Log Statistics ===")
        print(f"Total Logs: {total}")
        print(f"\nBreakdown:")
        for level, count in levels.most_common():
            percentage = (count / total) * 100
            print(f"  {level}: {count} ({percentage:.1f}%)")

def main():
    analyzer = LogAnalyzer('server.log')
    
    if not analyzer.logs:
        return
    
    print("=== Log Analyzer ===")
    print("Commands: level <LEVEL>, search <keyword>, errors, stats, hourly, top, range, exit\n")
    
    while True:
        command = input("analyzer> ").strip().split(maxsplit=1)
        
        if not command:
            continue
        
        cmd = command[0]
        
        if cmd == "level":
            if len(command) < 2:
                print("Usage: level <INFO|WARNING|ERROR|CRITICAL>")
            else:
                analyzer.filter_by_level(command[1])
        
        elif cmd == "search":
            if len(command) < 2:
                print("Usage: search <keyword>")
            else:
                analyzer.search(command[1])
        
        elif cmd == "errors":
            analyzer.errors_summary()
        
        elif cmd == "stats":
            analyzer.statistics()
        
        elif cmd == "hourly":
            analyzer.hourly_distribution()
        
        elif cmd == "top":
            analyzer.top_messages()
        
        elif cmd == "range":
            start = input("Start time (YYYY-MM-DD HH:MM:SS): ")
            end = input("End time (YYYY-MM-DD HH:MM:SS): ")
            analyzer.time_range(start, end)
        
        elif cmd == "exit":
            break
        
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
