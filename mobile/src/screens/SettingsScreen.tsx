import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity } from 'react-native';
import { api } from '../services/api';

export default function SettingsScreen() {
  const [apiKey, setApiKey] = useState('');
  const [saved, setSaved] = useState(false);

  const handleSave = async () => {
    if (apiKey) {
      await api.setApiKey(apiKey);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>設定</Text>
      
      <View style={styles.section}>
        <Text style={styles.label}>API Key</Text>
        <TextInput
          style={styles.input}
          value={apiKey}
          onChangeText={setApiKey}
          placeholder="輸入您的 API Key"
          secureTextEntry
        />
        <TouchableOpacity style={styles.button} onPress={handleSave}>
          <Text style={styles.buttonText}>儲存</Text>
        </TouchableOpacity>
        {saved && <Text style={styles.savedText}>已儲存！</Text>}
      </View>

      <View style={styles.section}>
        <Text style={styles.label}>語言</Text>
        <View style={styles.row}>
          <TouchableOpacity style={styles.langButton}>
            <Text>繁體中文</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.langButton}>
            <Text>English</Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.footer}>
        <Text style={styles.version}>Gold Analysis App v1.0.0</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F3F4F6',
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 24,
  },
  section: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#D1D5DB',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
  button: {
    backgroundColor: '#3B82F6',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 12,
  },
  buttonText: {
    color: 'white',
    fontWeight: '600',
  },
  savedText: {
    color: '#10B981',
    textAlign: 'center',
    marginTop: 8,
  },
  row: {
    flexDirection: 'row',
    gap: 12,
  },
  langButton: {
    flex: 1,
    paddingVertical: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#D1D5DB',
    borderRadius: 8,
  },
  footer: {
    marginTop: 'auto',
    alignItems: 'center',
  },
  version: {
    color: '#9CA3AF',
  },
});
