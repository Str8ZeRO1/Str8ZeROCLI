import React from 'react';
import { View, StyleSheet } from 'react-native';

export default function GlassPanel({ children }) {
  return (
    <View style={styles.glass}>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  glass: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderRadius: 20,
    padding: 20,
    shadowColor: '#00f0ff',
    shadowOpacity: 0.3,
    shadowRadius: 20,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.3)',
    margin: 10,
  },
});
