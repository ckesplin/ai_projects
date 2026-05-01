/**
 * MHS2 Save Transfer Tool - Main Application
 */
import { convertSave } from './src/conversion.js';

const FILE_SIZE_PC = 8421552;
const FILE_SIZE_NSW = 8421496;

let selectedFile = null;
let currentMode = 'pc-to-pc';

// DOM Elements
const modeOptions = document.querySelectorAll('input[name="mode"]');
const steamidGroup = document.getElementById('steamid-group');
const steamidInput = document.getElementById('steamid');
const steamidError = document.getElementById('steamid-error');
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const fileInfo = document.getElementById('file-info');
const convertBtn = document.getElementById('convert-btn');
const statusEl = document.getElementById('status');
const progressFill = document.getElementById('progress-fill');

// Mode selection
modeOptions.forEach(option => {
    option.addEventListener('change', (e) => {
        currentMode = e.target.value;
        updateSteamIdVisibility();
        updateConvertButton();
    });
});

function updateSteamIdVisibility() {
    if (currentMode === 'pc-to-nsw') {
        steamidGroup.classList.add('hidden');
        steamidError.textContent = '';
    } else {
        steamidGroup.classList.remove('hidden');
    }
}

// File selection via drag & drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    selectedFile = file;
    
    // Validate file size
    const validSizes = [FILE_SIZE_PC, FILE_SIZE_NSW];
    const isValidSize = validSizes.includes(file.size);
    
    if (isValidSize) {
        const format = file.size === FILE_SIZE_PC ? 'PC' : 'Switch';
        fileInfo.textContent = `${file.name} (${format} format, ${formatSize(file.size)})`;
        fileInfo.classList.add('has-file');
        steamidError.textContent = '';
    } else {
        fileInfo.textContent = '';
        fileInfo.classList.remove('has-file');
        steamidError.textContent = `Invalid file size: ${formatSize(file.size)} (expected ${formatSize(FILE_SIZE_PC)} for PC or ${formatSize(FILE_SIZE_NSW)} for Switch)`;
    }
    
    updateConvertButton();
}

function updateConvertButton() {
    let canConvert = selectedFile !== null;
    
    if (currentMode !== 'pc-to-nsw') {
        const steamId = BigInt(steamidInput.value || '0');
        if (steamId === 0n) {
            canConvert = false;
        }
    }
    
    convertBtn.disabled = !canConvert;
}

steamidInput.addEventListener('input', () => {
    const value = steamidInput.value.trim();
    if (value && !isValidSteamId(value)) {
        steamidError.textContent = 'Please enter a valid Steam ID (17-18 digits)';
    } else {
        steamidError.textContent = '';
    }
    updateConvertButton();
});

function isValidSteamId(value) {
    // Steam ID64 should be 17-18 digits
    return /^\d{17,18}$/.test(value);
}

function formatSize(bytes) {
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// Convert button
convertBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    setStatus('Reading file...', 'info');
    progressFill.style.width = '10%';
    
    try {
        const arrayBuffer = await selectedFile.arrayBuffer();
        
        const options = {
            targetSteamId: currentMode !== 'pc-to-nsw' ? BigInt(steamidInput.value) : null,
            convertToSwitch: currentMode === 'pc-to-nsw'
        };
        
        setStatus('Converting save file...', 'info');
        progressFill.style.width = '50%';
        
        // Small delay to allow UI to update
        await new Promise(resolve => setTimeout(resolve, 50));
        
        const result = await convertSave(arrayBuffer, options);
        
        setStatus('Creating download...', 'info');
        progressFill.style.width = '80%';
        
        downloadResult(result);
        
        setStatus('Conversion complete!', 'success');
        progressFill.style.width = '100%';
        
        // Reset after 3 seconds
        setTimeout(() => {
            progressFill.style.width = '0%';
        }, 3000);
        
    } catch (err) {
        setStatus('Error: ' + err.message, 'error');
        progressFill.style.width = '0%';
        console.error('Conversion error:', err);
    }
});

function downloadResult(data) {
    const blob = new Blob([data], { type: 'application/octet-stream' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    
    // Determine output filename
    let filename = selectedFile.name;
    const ext = filename.split('.').pop();
    const base = filename.slice(0, -(ext.length + 1));
    
    if (currentMode === 'pc-to-nsw') {
        filename = base + '_nsw.sav';
    } else if (currentMode === 'nsw-to-pc') {
        filename = base + '_pc.sav';
    } else {
        filename = base + '_converted.sav';
    }
    
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function setStatus(message, type) {
    statusEl.textContent = message;
    statusEl.className = 'status ' + type;
}

// Initialize
updateSteamIdVisibility();
updateConvertButton();