document.addEventListener('DOMContentLoaded', () => {
    
    // --- Upload Logic ---
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    let selectedFile = null;

    dropZone.addEventListener('click', () => fileInput.click());
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });
    
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            selectedFile = e.dataTransfer.files[0];
            updateDropZoneUI();
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            selectedFile = e.target.files[0];
            updateDropZoneUI();
        }
    });

    function updateDropZoneUI() {
        if (selectedFile) {
            dropZone.innerHTML = `<span class="drop-icon">✅</span><p class="highlight">${selectedFile.name}</p>`;
        }
    }

    uploadBtn.addEventListener('click', async () => {
        if (!selectedFile) {
            showToast('Veuillez sélectionner un fichier', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            uploadBtn.textContent = 'Archivage...';
            uploadBtn.disabled = true;
            
            const res = await fetch('/upload/', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            
            if (res.ok) {
                showToast(data.message || 'Fichier archivé avec succès', 'success');
                // Reset
                selectedFile = null;
                dropZone.innerHTML = `<span class="drop-icon">📄</span><p>Glissez-déposez votre fichier ici ou <span class="highlight">cliquez pour parcourir</span>.</p>`;
            } else {
                showToast(data.error || 'Erreur lors de l\'archivage', 'error');
            }
        } catch (error) {
            showToast('Erreur de connexion', 'error');
        } finally {
            uploadBtn.textContent = 'Archiver automatiquement';
            uploadBtn.disabled = false;
        }
    });

    // --- Create Department Logic ---
    document.getElementById('deptForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('deptName').value;
        const target_path = document.getElementById('deptPath').value;

        try {
            const res = await fetch('/departments/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, target_path })
            });
            const data = await res.json();

            if (res.ok) {
                showToast(`Département ${data.name} créé (ID: ${data.id})`, 'success');
                e.target.reset();
            } else {
                showToast(data.error || 'Erreur création département', 'error');
            }
        } catch (error) {
            showToast('Erreur serveur', 'error');
        }
    });

    // --- Create Rule Logic ---
    document.getElementById('ruleForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const extension = document.getElementById('ruleExt').value || null;
        const keyword = document.getElementById('ruleKeyword').value || null;
        const department_id = document.getElementById('ruleDeptId').value;

        try {
            const res = await fetch('/rules/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ extension, keyword, department_id: parseInt(department_id) })
            });
            const data = await res.json();

            if (res.ok) {
                showToast(`Règle ID ${data.id} ajoutée`, 'success');
                e.target.reset();
            } else {
                showToast(data.error || 'Erreur création règle', 'error');
            }
        } catch (error) {
            showToast('Erreur serveur', 'error');
        }
    });

    // --- Toast Notification System ---
    function showToast(message, type = 'success') {
        const area = document.getElementById('notificationArea');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'success' ? '✅' : '❌';
        toast.innerHTML = `<span>${icon}</span><p>${message}</p>`;
        
        area.appendChild(toast);

        // Remove after 4 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }
});
