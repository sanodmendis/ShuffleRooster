import pandas as pd
import random
import math

def shuffle_and_group_students(input_file='stdlist.csv', output_file='group.csv'):
    try:

        df = pd.read_csv(input_file)
        print(f'Loaded {len(df)} students from {input_file}')

        print('\nFirst 5 students:')
        print(df.head().to_string(index=False))

        while True:
            try:
                group_size = int(input(f'\nEnter number of students per group: '))
                if group_size > 0 and group_size <= len(df):
                    break
                else:
                    print(f'Please enter a number between 1 and {len(df)}')
            except ValueError:
                print('Please enter a valid number')

        num_groups = math.ceil(len(df) / group_size)
        print(f'\nCreating {num_groups} groups with {group_size} students each')
        print(f"(Last group may have fewer students if total doesn't divide evenly)")

        df_shuffled = df.sample(frac=1, random_state=random.randint(1, 10000)).reset_index(drop=True)

        df_shuffled['GROUP'] = [(i // group_size) + 1 for i in range(len(df_shuffled))]

        df_shuffled.to_csv(output_file, index=False)
        print(f'\nGroups saved to {output_file}')

        group_counts = df_shuffled['GROUP'].value_counts().sort_index()
        print(f'\nGroup Summary:')
        for group_num, count in group_counts.items():
            print(f'Group {group_num}: {count} students')

        print(f'\nSample of grouped data:')
        print(df_shuffled.head(10).to_string(index=False))

        return df_shuffled

    except FileNotFoundError:
        print(f'Error: {input_file} not found. Please make sure the file exists.')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    print('ShuffleRooster')
    print('=' * 30)
    shuffle_and_group_students()