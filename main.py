import customtkinter as ctk
import pandas as pd
import random
import math
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkinter import ttk
import os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

class mainWindow:
    def __init__(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')
        
        self.root = ctk.CTk()
        self.root.title('ShuffleRooster - Student Group Shuffler')
        self.root.geometry('800x700')
        self.root.state('zoomed')
        
        self.df = None
        self.grouped_df = None
        self.tree = None
        
        self.initUI()
        
    def initUI(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
                
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill='x', padx=20, pady=10)
        
        self.file_label = ctk.CTkLabel(file_frame, text='No file selected')
        self.file_label.pack(side='left', padx=20, pady=15)
        select_file_btn = ctk.CTkButton(file_frame, text='Select File', command=self.select_file)
        select_file_btn.pack(side='right', padx=20, pady=15)
        
        self.student_info_label = ctk.CTkLabel(main_frame, text='')
        self.student_info_label.pack(pady=10)
        
        group_frame = ctk.CTkFrame(main_frame)
        group_frame.pack(fill='x', padx=20, pady=10)
        
        ctk.CTkLabel(group_frame, text='Students per group:').pack(side='left', padx=20, pady=15)
        
        self.group_size_var = ctk.StringVar(value='4')
        self.group_size_entry = ctk.CTkEntry(group_frame, textvariable=self.group_size_var, width=100)
        self.group_size_entry.pack(side='left', padx=10, pady=15)
        create_groups_btn = ctk.CTkButton(group_frame, text='Create Groups', command=self.create_groups)
        create_groups_btn.pack(side='right', padx=20, pady=15)
        
        tree_frame = ctk.CTkFrame(main_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=(20, 10))

        self.tree = ttk.Treeview(tree_frame, show='headings', height=15)
        self.tree.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill='x', padx=20, pady=10)
        save_frame = ctk.CTkFrame(button_frame)
        save_frame.pack(pady=15)
        ctk.CTkLabel(save_frame, text='Save as:').pack(side='left', padx=(10, 5), pady=15)
        self.save_format_var = ctk.StringVar(value='CSV')
        self.save_menu = ctk.CTkOptionMenu(
            save_frame,
            values=['CSV', 'Excel (XLSX)', 'Excel (XLS)', 'PDF'],
            variable=self.save_format_var,
            command=self.save_groups
        )
        self.save_menu.pack(side='left', padx=10, pady=15)
        
    def update_treeview(self, dataframe):
        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = list(dataframe.columns)

        for col in dataframe.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        for _, row in dataframe.iterrows():
            self.tree.insert('', 'end', values=list(row))
            
    def select_file(self):
        file_path = fd.askopenfilename(
            title='Select file',
            filetypes=[
                ('All supported', '*.csv;*.xlsx;*.xls'),
                ('CSV files', '*.csv'),
                ('Excel files', '*.xlsx;*.xls'),
                ('All files', '*.*')
            ]
        )
        if file_path:
            try:
                file_ext = os.path.splitext(file_path)[1].lower()
    
                if file_ext == '.csv':
                    self.df = pd.read_csv(file_path)
                elif file_ext in ['.xlsx', '.xls']:
                    self.df = pd.read_excel(file_path)
                else:
                    raise ValueError(f'Unsupported file format: {file_ext}')
    
                filename = os.path.basename(file_path)
                self.file_label.configure(text=f'File: {filename}')
                self.student_info_label.configure(text=f'Loaded {len(self.df)} students')
        
                self.update_treeview(self.df)
        
            except Exception as e:
                mb.showerror('Error', f'Failed to load file: {str(e)}')
                
    def create_groups(self):
        if self.df is None:
            mb.showwarning('Warning', 'Please select a file first')
            return
        
        try:
            group_size = int(self.group_size_var.get())
    
            if group_size <= 0 or group_size > len(self.df):
                mb.showerror('Error', f'Group size must be between 1 and {len(self.df)}')
                return
    
        except ValueError:
            mb.showerror('Error', 'Please enter a valid number for group size')
            return
        
        df_shuffled = self.df.sample(frac=1, random_state=random.randint(1, 10000)).reset_index(drop=True)
        df_shuffled['GROUP'] = [(i // group_size) + 1 for i in range(len(df_shuffled))]
        
        last_group = df_shuffled['GROUP'].max()
        last_group_size = len(df_shuffled[df_shuffled['GROUP'] == last_group])
        min_group_size = (group_size // 2) + 1
        
        if last_group_size < min_group_size and last_group > 1:
            last_group_students = df_shuffled[df_shuffled['GROUP'] == last_group].index.tolist()
            available_groups = list(range(1, last_group))
        
            for student_idx in last_group_students:
                new_group = random.choice(available_groups)
                df_shuffled.loc[student_idx, 'GROUP'] = new_group
        
        self.grouped_df = df_shuffled.sort_values('GROUP').reset_index(drop=True)
        self.student_info_label.configure(text=f'Created {self.grouped_df["GROUP"].nunique()} groups')
        self.update_treeview(self.grouped_df)
        
    def save_groups(self, choice=None):
        if self.grouped_df is None:
            mb.showwarning('Warning', 'Please create groups first')
            return
        
        format_choice = self.save_format_var.get()
        
        if format_choice == 'CSV':
            file_path = fd.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])

            if file_path:
                self.grouped_df.to_csv(file_path, index=False)
                mb.showinfo('Success', f'Groups saved to {file_path}')
        
        elif format_choice == 'Excel (XLSX)':
            file_path = fd.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel files', '*.xlsx'), ('All files', '*.*')])
        
            if file_path:
                self.grouped_df.to_excel(file_path, index=False)
                mb.showinfo('Success', f'Groups saved to {file_path}')
    
        elif format_choice == 'Excel (XLS)':
            file_path = fd.asksaveasfilename(defaultextension='.xls', filetypes=[('Excel files', '*.xls'), ('All files', '*.*')])
    
            if file_path:
                self.grouped_df.to_excel(file_path, index=False)
                mb.showinfo('Success', f'Groups saved to {file_path}')
    
        elif format_choice == 'PDF':
            file_path = fd.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF files', '*.pdf'), ('All files', '*.*')])
    
            if file_path:
                self.save_as_pdf(file_path)
                mb.showinfo('Success', f'Groups saved to {file_path}')
    
    def save_as_pdf(self, file_path):
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        title = Paragraph("Student Groups", styles['Title'])

        elements.append(title)
        data = [list(self.grouped_df.columns)]
        
        for _, row in self.grouped_df.iterrows():
            data.append(list(row.astype(str)))
        
        table = Table(data)
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        doc.build(elements)
                
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = mainWindow()
    app.run()