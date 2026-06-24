# 按鈕、輸入框與表單

## 使用者輸入的核心元件

表單是 App 與使用者互動的核心方式。React Native 提供了一系列輸入元件，讓開發者可以建立完整的表單體驗。

## Button：基本按鈕

React Native 內建的 `Button` 元件是跨平台按鈕的最小共用元件：

```jsx
import { Button, Alert } from "react-native";

const MyButton = () => (
    <View style={styles.container}>
        <Button
            title="基本按鈕"
            onPress={() => Alert.alert("按鈕被按下")}
            color="#007AFF"
            disabled={false}
        />
    </View>
);
```

`Button` 的樣式有限，實際開發中更常用 `TouchableOpacity` 或 `Pressable`：

```jsx
import { TouchableOpacity, Text, StyleSheet } from "react-native";

const CustomButton = ({
    title,
    onPress,
    variant = "primary",
    disabled,
}) => (
    <TouchableOpacity
        style={[
            styles.button,
            styles[variant],
            disabled && styles.disabled,
        ]}
        onPress={onPress}
        disabled={disabled}
        activeOpacity={0.7}
    >
        <Text style={[
            styles.text,
            variant === "outline" && styles.outlineText,
            disabled && styles.disabledText,
        ]}>
            {title}
        </Text>
    </TouchableOpacity>
);
```

## TextInput：文字輸入

`TextInput` 是 React Native 的核心輸入元件：

```jsx
import { TextInput, View, StyleSheet } from "react-native";
import { useState } from "react";

const LoginForm = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [secureText, setSecureText] = useState(true);

    return (
        <View style={styles.form}>
            <TextInput
                style={styles.input}
                placeholder="電子郵件"
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
                autoCorrect={false}
                returnKeyType="next"
            />
            <View style={styles.passwordContainer}>
                <TextInput
                    style={styles.input}
                    placeholder="密碼"
                    value={password}
                    onChangeText={setPassword}
                    secureTextEntry={secureText}
                    autoCapitalize="none"
                    returnKeyType="done"
                />
                <TouchableOpacity
                    style={styles.eyeIcon}
                    onPress={() => setSecureText(!secureText)}
                >
                    <Text>{secureText ? "顯示" : "隱藏"}</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};
```

### TextInput 常用屬性

```jsx
<TextInput
    // 基本
    value={text}
    onChangeText={setText}
    placeholder="請輸入..."

    // 鍵盤類型
    keyboardType="default"       // 預設
              | "email-address"  // 電子郵件
              | "numeric"        // 數字
              | "phone-pad"      // 電話
              | "url"            // 網址

    // 行為
    secureTextEntry={false}      // 密碼遮罩
    autoFocus={true}             // 自動聚焦
    multiline={false}            // 多行
    numberOfLines={3}            // 行數（multiline 時）
    maxLength={100}              // 最大字元數

    // 樣式
    textAlign="left"             // 文字對齊
    returnKeyType="done"         // 返回鍵類型
/>
```

## 表單驗證

實作表單驗證是常見需求：

```jsx
import { useState } from "react";
import { View, TextInput, Text, StyleSheet } from "react-native";

type ValidationRule = {
    required?: boolean;
    minLength?: number;
    pattern?: RegExp;
    message: string;
};

const useFormField = (initial: string, rules: ValidationRule[]) => {
    const [value, setValue] = useState(initial);
    const [error, setError] = useState("");

    const validate = () => {
        for (const rule of rules) {
            if (rule.required && !value.trim()) {
                setError(rule.message);
                return false;
            }
            if (rule.minLength && value.length < rule.minLength) {
                setError(rule.message);
                return false;
            }
            if (rule.pattern && !rule.pattern.test(value)) {
                setError(rule.message);
                return false;
            }
        }
        setError("");
        return true;
    };

    return { value, setValue, error, validate };
};

const RegisterForm = () => {
    const email = useFormField("", [
        { required: true, message: "請輸入電子郵件" },
        {
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: "請輸入有效的電子郵件",
        },
    ]);
    const password = useFormField("", [
        { required: true, message: "請輸入密碼" },
        { minLength: 6, message: "密碼至少需要 6 個字元" },
    ]);

    const handleSubmit = () => {
        const isEmailValid = email.validate();
        const isPasswordValid = password.validate();
        if (isEmailValid && isPasswordValid) {
            // 送出表單
        }
    };

    return (
        <View style={styles.form}>
            <TextInput
                style={styles.input}
                placeholder="電子郵件"
                value={email.value}
                onChangeText={email.setValue}
            />
            {email.error && <Text style={styles.error}>{email.error}</Text>}

            <TextInput
                style={styles.input}
                placeholder="密碼"
                secureTextEntry
                value={password.value}
                onChangeText={password.setValue}
            />
            {password.error && <Text style={styles.error}>{password.error}</Text>}

            <CustomButton title="註冊" onPress={handleSubmit} />
        </View>
    );
};
```

## Switch 與 Slider

```jsx
import { Switch, Slider } from "react-native";

const SettingsForm = () => {
    const [notifications, setNotifications] = useState(true);
    const [volume, setVolume] = useState(0.5);

    return (
        <View>
            <View style={styles.row}>
                <Text>開啟通知</Text>
                <Switch
                    value={notifications}
                    onValueChange={setNotifications}
                    trackColor={{ false: "#ccc", true: "#34C759" }}
                />
            </View>
            <View style={styles.row}>
                <Text>音量：{Math.round(volume * 100)}%</Text>
                <Slider
                    style={{ flex: 1 }}
                    value={volume}
                    onValueChange={setVolume}
                    minimumValue={0}
                    maximumValue={1}
                    step={0.1}
                />
            </View>
        </View>
    );
};
```

---

## 延伸閱讀

- [TextInput API 文件](https://www.google.com/search?q=React+Native+TextInput)
- [React Native 表單驗證](https://www.google.com/search?q=React+Native+form+validation)
- [Pressable 元件指南](https://www.google.com/search?q=React+Native+Pressable)
