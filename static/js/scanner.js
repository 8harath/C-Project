/**
 * Barcode Scanner using QuaggaJS
 * Handles EAN-13 barcode detection and sale processing
 */

let isScanning = false;
let lastDetectedBarcode = null;
let lastDetectionTime = 0;
const DETECTION_COOLDOWN = 2000; // 2 seconds cooldown between detections

// Audio feedback
const beepSound = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiDcIF2i58OScTgwOUavm8LNlHAU2kdvyy30tBSN2x+/ekUALFV6069+oVhQKRp7f8r5sIQUrlM7y2Ic3CBZpuezjm08MDFCr5O+zZRsFN5Ha8sp9LQUjdsXv3pFAChVetOvfqFYUCkae3++9bCAFKpPO8tiHNwgWabns45lPDAhPq+Xvs2UbBzaR2/LKfS0FI3bF79+RQAoVXrPr4KhWFApGnt/vvWwgBSqTzvLYhzcIFmm57OOZTwsJT6vl77NlGwc2kdvyynyuBCN2xe/fkUAKFV607N+oVhQLRp7f771sIAUqk87y2Ic3CBZpuevsm08LCU+r5e6yZRsHNpHa88l8rgQjdsXv35FAChVetOzfp1YUC0ae3++9bCAFKpPO8tiHNwgWabns45lPCwlPq+XusmUbBzaR2vPJfK4EI3bF79+RQAoUXrTs4KdWFAtGnt/vvWwgBSqTzvLYhzcIFmm57OOZTwsIT6vl7rJlGwc2kdryyny');

// Initialize scanner
function initScanner() {
    Quagga.init({
        inputStream: {
            name: "Live",
            type: "LiveStream",
            target: document.querySelector('#interactive'),
            constraints: {
                width: 640,
                height: 480,
                facingMode: "environment" // Use rear camera on mobile
            },
        },
        decoder: {
            readers: ["ean_reader"] // EAN-13 barcode format
        },
        locate: true,
        locator: {
            patchSize: "medium",
            halfSample: true
        },
        numOfWorkers: navigator.hardwareConcurrency || 4,
        frequency: 10,
    }, function (err) {
        if (err) {
            console.error("Error initializing QuaggaJS:", err);
            handleCameraError(err);
            return;
        }
        console.log("QuaggaJS initialized successfully");
        Quagga.start();
        isScanning = true;
        updateScannerButtons();
    });

    // Handle barcode detection
    Quagga.onDetected(handleBarcodeDetection);
}

// Handle camera permission errors
function handleCameraError(err) {
    const alertDiv = document.getElementById('camera-permission-alert');
    if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        alertDiv.style.display = 'block';
        alertDiv.innerHTML = `
            <h5><i class="bi bi-exclamation-triangle"></i> Camera Permission Denied</h5>
            <p>Please allow camera access in your browser settings to use the barcode scanner.</p>
            <p>You can use the manual barcode entry form below instead.</p>
        `;
    } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        alertDiv.style.display = 'block';
        alertDiv.innerHTML = `
            <h5><i class="bi bi-exclamation-triangle"></i> No Camera Found</h5>
            <p>No camera device was found on your system.</p>
            <p>Please use the manual barcode entry form below.</p>
        `;
    } else {
        alertDiv.style.display = 'block';
        alertDiv.innerHTML = `
            <h5><i class="bi bi-exclamation-triangle"></i> Camera Error</h5>
            <p>An error occurred while accessing the camera: ${err.message || err}</p>
            <p>Please use the manual barcode entry form below.</p>
        `;
    }
}

// Handle barcode detection
function handleBarcodeDetection(result) {
    const code = result.codeResult.code;
    const currentTime = Date.now();

    // Prevent duplicate detections
    if (code === lastDetectedBarcode && (currentTime - lastDetectionTime) < DETECTION_COOLDOWN) {
        return;
    }

    lastDetectedBarcode = code;
    lastDetectionTime = currentTime;

    // Validate EAN-13 format
    if (code.length !== 13 || !/^\d+$/.test(code)) {
        console.warn("Invalid barcode format:", code);
        return;
    }

    console.log("Barcode detected:", code);

    // Play beep sound
    try {
        beepSound.play().catch(e => console.log("Could not play beep sound:", e));
    } catch (e) {
        console.log("Audio playback not supported");
    }

    // Display result
    displayBarcodeResult(code);

    // Fetch medicine details
    fetchMedicineDetails(code);
}

// Display barcode result
function displayBarcodeResult(barcode) {
    const resultDiv = document.getElementById('barcode-result');
    resultDiv.innerHTML = `
        <div class="alert alert-success">
            <h5><i class="bi bi-check-circle"></i> Barcode Detected!</h5>
            <p class="mb-0"><strong>Barcode:</strong> ${barcode}</p>
            <p class="mb-0 mt-2"><small>Fetching medicine details...</small></p>
        </div>
    `;
}

// Fetch medicine details from API
function fetchMedicineDetails(barcode) {
    fetch(`/medicines/api/barcode/${barcode}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Medicine not found (${response.status})`);
            }
            return response.json();
        })
        .then(data => {
            showSaleConfirmation(data, barcode);
        })
        .catch(error => {
            console.error("Error fetching medicine:", error);
            const resultDiv = document.getElementById('barcode-result');
            resultDiv.innerHTML = `
                <div class="alert alert-danger">
                    <h5><i class="bi bi-x-circle"></i> Medicine Not Found</h5>
                    <p class="mb-0"><strong>Barcode:</strong> ${barcode}</p>
                    <p class="mb-0">No medicine found with this barcode.</p>
                </div>
            `;
        });
}

// Show sale confirmation modal
function showSaleConfirmation(medicine, barcode) {
    if (medicine.is_expired) {
        const resultDiv = document.getElementById('barcode-result');
        resultDiv.innerHTML = `
            <div class="alert alert-danger">
                <h5><i class="bi bi-exclamation-triangle"></i> Expired Medicine</h5>
                <p class="mb-0"><strong>${medicine.name}</strong> has expired and cannot be sold.</p>
                <p class="mb-0"><small>Expiry Date: ${medicine.expiry_date}</small></p>
            </div>
        `;
        return;
    }

    if (medicine.stock === 0) {
        const resultDiv = document.getElementById('barcode-result');
        resultDiv.innerHTML = `
            <div class="alert alert-warning">
                <h5><i class="bi bi-exclamation-triangle"></i> Out of Stock</h5>
                <p class="mb-0"><strong>${medicine.name}</strong> is currently out of stock.</p>
            </div>
        `;
        return;
    }

    // Populate modal
    const modalBody = document.getElementById('sale-modal-body');
    modalBody.innerHTML = `
        <div class="mb-3">
            <h5>${medicine.name}</h5>
            <p class="text-muted mb-1">${medicine.manufacturer}</p>
            <p class="text-muted mb-1"><small>Category: ${medicine.category}</small></p>
            <p class="text-muted mb-1"><small>Barcode: ${barcode}</small></p>
        </div>
        <div class="mb-3">
            <label for="sale-quantity" class="form-label">Quantity</label>
            <input type="number" class="form-control" id="sale-quantity"
                   value="1" min="1" max="${medicine.stock}" required>
            <small class="text-muted">Available stock: ${medicine.stock}</small>
        </div>
        <div class="alert alert-info">
            <p class="mb-1"><strong>Unit Price:</strong> ₹${medicine.price.toFixed(2)}</p>
            <p class="mb-0"><strong>Total:</strong> ₹<span id="modal-total">${medicine.price.toFixed(2)}</span></p>
        </div>
    `;

    // Update total on quantity change
    const quantityInput = document.getElementById('sale-quantity');
    quantityInput.addEventListener('input', function () {
        const quantity = parseInt(this.value) || 1;
        const total = (medicine.price * quantity).toFixed(2);
        document.getElementById('modal-total').textContent = total;
    });

    // Store medicine data for confirmation
    document.getElementById('confirm-sale-btn').dataset.barcode = barcode;
    document.getElementById('confirm-sale-btn').dataset.medicineId = medicine.medicine_id;

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('saleModal'));
    modal.show();
}

// Confirm and record sale
function confirmSale() {
    const barcode = document.getElementById('confirm-sale-btn').dataset.barcode;
    const quantity = parseInt(document.getElementById('sale-quantity').value);

    if (!barcode || !quantity || quantity < 1) {
        alert('Invalid quantity');
        return;
    }

    // Send sale request
    fetch('/sell/barcode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            barcode: barcode,
            quantity: quantity
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Close modal
                bootstrap.Modal.getInstance(document.getElementById('saleModal')).hide();

                // Show success message
                const resultDiv = document.getElementById('barcode-result');
                resultDiv.innerHTML = `
                    <div class="alert alert-success">
                        <h5><i class="bi bi-check-circle"></i> Sale Recorded!</h5>
                        <p class="mb-2">${data.message}</p>
                        ${data.low_stock ? `<p class="mb-2"><strong>Warning:</strong> Stock is low (${data.remaining_stock} remaining)</p>` : ''}
                        <a href="${data.receipt_url}" class="btn btn-primary btn-sm">
                            <i class="bi bi-receipt"></i> View Receipt
                        </a>
                    </div>
                `;

                // Reset detection
                lastDetectedBarcode = null;
            } else {
                throw new Error(data.error || 'Sale failed');
            }
        })
        .catch(error => {
            console.error('Error recording sale:', error);
            alert('Error recording sale: ' + error.message);
        });
}

// Stop scanner
function stopScanner() {
    if (isScanning) {
        Quagga.stop();
        isScanning = false;
        updateScannerButtons();
        console.log("Scanner stopped");
    }
}

// Update scanner control buttons
function updateScannerButtons() {
    const startBtn = document.getElementById('start-scan-btn');
    const stopBtn = document.getElementById('stop-scan-btn');

    if (isScanning) {
        startBtn.style.display = 'none';
        stopBtn.style.display = 'inline-block';
    } else {
        startBtn.style.display = 'inline-block';
        stopBtn.style.display = 'none';
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function () {
    const startBtn = document.getElementById('start-scan-btn');
    const stopBtn = document.getElementById('stop-scan-btn');
    const confirmBtn = document.getElementById('confirm-sale-btn');

    if (startBtn) {
        startBtn.addEventListener('click', initScanner);
    }

    if (stopBtn) {
        stopBtn.addEventListener('click', stopScanner);
    }

    if (confirmBtn) {
        confirmBtn.addEventListener('click', confirmSale);
    }

    // Cleanup on page unload
    window.addEventListener('beforeunload', function () {
        if (isScanning) {
            stopScanner();
        }
    });
});
