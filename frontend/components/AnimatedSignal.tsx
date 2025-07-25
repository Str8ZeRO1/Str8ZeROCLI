import React, { useEffect } from 'react';
import { View, StyleSheet, Animated } from 'react-native';

export default function AnimatedSignal() {
  const animation = new Animated.Value(0);
  
  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(animation, {
          toValue: 1,
          duration: 1500,
          useNativeDriver: true,
        }),
        Animated.timing(animation, {
          toValue: 0,
          duration: 1500,
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, []);
  
  return (
    <Animated.View
      style={[
        styles.signal,
        {
          opacity: animation,
          transform: [
            {
              scale: animation.interpolate({
                inputRange: [0, 1],
                outputRange: [1, 1.2],
              }),
            },
          ],
        },
      ]}
    />
  );
}

const styles = StyleSheet.create({
  signal: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: '#00f0ff',
    margin: 5,
  },
});
