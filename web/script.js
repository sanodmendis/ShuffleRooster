class ShuffleRooster {
    constructor() {
        this.data = null;
        this.groupedData = null;
        this.currentFormat = 'xlsx';
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.fileInput = document.getElementById('fileInput');
        this.selectFileBtn = document.getElementById('selectFileBtn');
        this.clearFileBtn = document.getElementById('clearFileBtn');
        this.fileLabel = document.getElementById('fileLabel');
        this.studentInfo = document.getElementById('studentInfo');
        this.groupSizeInput = document.getElementById('groupSize');
        this.createGroupsBtn = document.getElementById('createGroupsBtn');
        this.saveBtn = document.getElementById('saveBtn');
        this.saveDropdownBtn = document.getElementById('saveDropdownBtn');
        this.saveDropdownMenu = document.getElementById('saveDropdownMenu');
        this.mobileSaveBtn = document.getElementById('mobileSaveBtn');
        this.mobileSaveDropdownBtn = document.getElementById('mobileSaveDropdownBtn');
        this.mobileSaveDropdownMenu = document.getElementById('mobileSaveDropdownMenu');
        this.tableHead = document.getElementById('tableHead');
        this.tableBody = document.getElementById('tableBody');
        this.notification = document.getElementById('notification');
        this.numberUp = document.querySelector('.number-up');
        this.numberDown = document.querySelector('.number-down');
        this.shuffleSwitch = document.getElementById('shuffleSwitch');
    }

    bindEvents() {
        this.selectFileBtn.addEventListener('click', () => this.fileInput.click());
        this.clearFileBtn.addEventListener('click', () => this.clearFile());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.createGroupsBtn.addEventListener('click', () => this.createGroups());
        this.saveBtn.addEventListener('click', () => this.saveFile());
        this.saveDropdownBtn.addEventListener('click', (e) => this.toggleDropdown(e, this.saveDropdownMenu));
        this.mobileSaveBtn.addEventListener('click', () => this.saveFile());
        this.mobileSaveDropdownBtn.addEventListener('click', (e) => this.toggleDropdown(e, this.mobileSaveDropdownMenu));
        
        this.numberUp.addEventListener('click', () => this.adjustNumber(1));
        this.numberDown.addEventListener('click', () => this.adjustNumber(-1));
        
        document.querySelectorAll('.dropdown-item').forEach(item => {
            item.addEventListener('click', (e) => this.selectFormat(e));
        });
        
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.btn-group')) {
                this.closeDropdown();
            }
        });
    }

    clearFile() {
        this.data = null;
        this.groupedData = null;
        this.fileInput.value = '';
        this.fileLabel.textContent = 'No file selected';
        this.studentInfo.textContent = '';
        this.groupSizeInput.max = 100;
        this.updateTable([]);
        this.showNotification('File cleared successfully!', 'success');
    }

    adjustNumber(direction) {
        let value = parseInt(this.groupSizeInput.value) || 0;
        value += direction;
        
        if (value < 1) value = 1;
        if (value > 100) value = 100;
        
        this.groupSizeInput.value = value;
    }

    toggleDropdown(e, dropdownMenu) {
        e.stopPropagation();
        this.closeDropdown();
        dropdownMenu.classList.toggle('show');
    }

    closeDropdown() {
        this.saveDropdownMenu.classList.remove('show');
        this.mobileSaveDropdownMenu.classList.remove('show');
    }

    selectFormat(e) {
        this.currentFormat = e.currentTarget.dataset.format;
        this.updateSaveButtonText();
        this.closeDropdown();
        this.showNotification(`Format changed to ${this.currentFormat.toUpperCase()}`, 'success');
    }

    updateSaveButtonText() {
        const formatNames = {
            'xlsx': 'Save as XLSX',
            'xls': 'Save as XLS', 
            'csv': 'Save as CSV'
        };
        const buttonText = `<i class="fas fa-download"></i> ${formatNames[this.currentFormat]}`;
        this.saveBtn.innerHTML = buttonText;
        this.mobileSaveBtn.innerHTML = buttonText;
    }

    showNotification(message, type = 'success') {
        this.notification.textContent = message;
        this.notification.className = `notification ${type} show`;
        
        setTimeout(() => {
            this.notification.classList.remove('show');
        }, 3000);
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;

        const fileName = file.name;
        const fileExtension = fileName.split('.').pop().toLowerCase();

        if (!['csv', 'xlsx', 'xls'].includes(fileExtension)) {
            this.showNotification('Please select a CSV or Excel file', 'error');
            return;
        }

        this.fileLabel.textContent = `File: ${fileName}`;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                if (fileExtension === 'csv') {
                    this.parseCSV(e.target.result);
                } else {
                    this.parseExcel(e.target.result);
                }
            } catch (error) {
                this.showNotification('Error reading file: ' + error.message, 'error');
            }
        };

        if (fileExtension === 'csv') {
            reader.readAsText(file);
        } else {
            reader.readAsArrayBuffer(file);
        }
    }

    parseCSV(csvText) {
        const lines = csvText.split('\n').filter(line => line.trim());
        if (lines.length === 0) {
            throw new Error('File is empty');
        }

        const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
        const data = [];

        for (let i = 1; i < lines.length; i++) {
            const values = lines[i].split(',').map(v => v.trim().replace(/"/g, ''));
            if (values.length === headers.length) {
                const row = {};
                headers.forEach((header, index) => {
                    row[header] = values[index];
                });
                data.push(row);
            }
        }

        this.data = data;
        this.updateUI();
        this.updateTable(this.data);
    }

    parseExcel(arrayBuffer) {
        const workbook = XLSX.read(arrayBuffer, { type: 'array' });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet);

        if (jsonData.length === 0) {
            throw new Error('File is empty or has no data');
        }

        this.data = jsonData;
        this.updateUI();
        this.updateTable(this.data);
    }

    updateUI() {
        this.studentInfo.textContent = `Loaded ${this.data.length} students`;
        this.groupSizeInput.max = this.data.length;
    }

    updateTable(data) {
        this.tableHead.innerHTML = '';
        this.tableBody.innerHTML = '';

        if (!data || data.length === 0) return;

        const headers = Object.keys(data[0]);
        const headerRow = document.createElement('tr');
        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });
        this.tableHead.appendChild(headerRow);

        data.forEach(row => {
            const tr = document.createElement('tr');
            headers.forEach(header => {
                const td = document.createElement('td');
                td.textContent = row[header] || '';
                tr.appendChild(td);
            });
            this.tableBody.appendChild(tr);
        });
    }

    createGroups() {
        if (!this.data) {
            this.showNotification('Please select a file first', 'warning');
            return;
        }

        const groupSize = parseInt(this.groupSizeInput.value);
        if (groupSize <= 0 || groupSize > this.data.length) {
            this.showNotification(`Group size must be between 1 and ${this.data.length}`, 'error');
            return;
        }

        const shouldShuffle = this.shuffleSwitch.checked;
        let processedData = [...this.data];
        
        if (shouldShuffle) {
            processedData = processedData.sort(() => Math.random() - 0.5);
        }
        
        processedData.forEach((student, index) => {
            student.GROUP = Math.floor(index / groupSize) + 1;
        });

        const lastGroup = Math.max(...processedData.map(s => s.GROUP));
        const lastGroupStudents = processedData.filter(s => s.GROUP === lastGroup);
        const minGroupSize = Math.floor(groupSize / 2) + 1;

        if (lastGroupStudents.length < minGroupSize && lastGroup > 1) {
            const availableGroups = Array.from({length: lastGroup - 1}, (_, i) => i + 1);
            lastGroupStudents.forEach(student => {
                const randomGroup = availableGroups[Math.floor(Math.random() * availableGroups.length)];
                student.GROUP = randomGroup;
            });
        }

        this.groupedData = processedData.sort((a, b) => a.GROUP - b.GROUP);
        
        const numGroups = Math.max(...this.groupedData.map(s => s.GROUP));
        this.studentInfo.textContent = `Created ${numGroups} groups`;
        
        this.updateTable(this.groupedData);
        this.showNotification('Groups created successfully!');
    }

    saveFile() {
        if (!this.groupedData) {
            this.showNotification('Please create groups first', 'warning');
            return;
        }

        const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
        const filename = `grouped_${timestamp}`;

        if (this.currentFormat === 'csv') {
            this.downloadCSV(filename);
        } else {
            this.downloadExcel(filename, this.currentFormat);
        }
    }

    downloadCSV(filename) {
        const headers = Object.keys(this.groupedData[0]);
        const csvContent = [
            headers.join(','),
            ...this.groupedData.map(row => 
                headers.map(header => `"${row[header] || ''}"`).join(',')
            )
        ].join('\n');

        this.downloadFile(csvContent, filename + '.csv', 'text/csv');
        this.showNotification('CSV file downloaded successfully!');
    }

    downloadExcel(filename, format) {
        const worksheet = XLSX.utils.json_to_sheet(this.groupedData);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Groups');

        const extension = format === 'xls' ? '.xls' : '.xlsx';
        XLSX.writeFile(workbook, filename + extension);
        this.showNotification('Excel file downloaded successfully!');
    }

    downloadFile(content, filename, contentType) {
        const blob = new Blob([content], { type: contentType });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ShuffleRooster();
});