import React, { useEffect } from 'react';

const TextCodeGenerator = () => {
    // Reference to DOM elements
    let inputTextArea;
    let outputTextArea;
    let toolSelect;
    let generateBtn;
    let resetBtn;
    let copyBtn;

    useEffect(() => {
        // Get references to DOM elements
        inputTextArea = document.getElementById('inputText');
        outputTextArea = document.getElementById('outputText');
        toolSelect = document.getElementById('toolSelect');
        generateBtn = document.getElementById('generateBtn');
        resetBtn = document.getElementById('resetBtn');
        copyBtn = document.getElementById('copyBtn');
        
        // Add event listeners
        generateBtn.addEventListener('click', handleGenerate);
        resetBtn.addEventListener('click', handleReset);
        copyBtn.addEventListener('click', handleCopy);
        
        // Clean up event listeners when component unmounts
        return () => {
            generateBtn.removeEventListener('click', handleGenerate);
            resetBtn.removeEventListener('click', handleReset);
            copyBtn.removeEventListener('click', handleCopy);
        };
    }, []);
    
    // Sanitize text to prevent harmful content
    const sanitizeText = (text) => {
        // Basic sanitization - strip HTML tags
        const sanitized = text.replace(/<[^>]*>?/gm, '');
        // You can add more sanitization rules as needed
        return sanitized;
    };

    // Process text based on selected tool
    const processText = (inputText, selectedTool) => {
        if (!inputText) {
            return 'Please enter text to process';
        }
        
        // Sanitize input first
        const sanitizedText = sanitizeText(inputText);
        
        if (!sanitizedText) {
            return 'Text contained only unsafe content that was removed';
        }
        
        let processedResult;
        
        // Process based on selected tool
        switch(selectedTool) {
            case 'uppercase':
                processedResult = sanitizedText.toUpperCase();
                break;
            case 'lowercase':
                processedResult = sanitizedText.toLowerCase();
                break;
            case 'reverse':
                processedResult = sanitizedText.split('').reverse().join('');
                break;
            default:
                processedResult = 'Unknown tool selected';
        }
        
        return processedResult;
    };
    
    // Event Handlers
    const handleGenerate = (e) => {
        e.preventDefault();
        
        if (!inputTextArea || !outputTextArea || !toolSelect) {
            return;
        }
        
        const inputText = inputTextArea.value;
        const selectedTool = toolSelect.value;
        
        const result = processText(inputText, selectedTool);
        outputTextArea.value = result;
    };
    
    const handleReset = () => {
        if (inputTextArea && outputTextArea) {
            inputTextArea.value = '';
            outputTextArea.value = '';
        }
    };
    
    const handleCopy = () => {
        if (outputTextArea) {
            outputTextArea.select();
            document.execCommand('copy');
            // Optional: visual feedback
            alert('Copied to clipboard!');
        }
    };

    // This component doesn't render any UI of its own
    // It just connects to the existing UI elements
    return null;
};

export default TextCodeGenerator;
