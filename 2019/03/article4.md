# 超參數調優

## 超參數種類

- **網路架構**：層數、每層神經元數
- **訓練參數**：學習率、批次大小、Epoch 數
- **正規化**：Dropout 率、L1/L2 參數

## 網格搜尋（Grid Search）

窮舉所有超參數組合：

```python
from sklearn.model_selection import GridSearchCV
from tensorflow import keras
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier

def create_model(hidden_units=64, learning_rate=0.001):
    model = keras.Sequential([
        layers.Dense(hidden_units, activation='relu', input_shape=(784,)),
        layers.Dense(10, activation='softmax')
    ])
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

param_grid = {
    'hidden_units': [32, 64, 128],
    'learning_rate': [0.001, 0.01]
}

model = KerasClassifier(build_fn=create_model, epochs=10, verbose=0)

grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=3,
    n_jobs=-1
)

grid_search.fit(x_train, y_train)

print(f"最佳參數: {grid_search.best_params_}")
print(f"最佳分數: {grid_search.best_score_:.2%}")
```

## 隨機搜尋（Random Search）

在參數範圍內隨機抽樣：

```python
from scipy.stats import uniform, randint

param_dist = {
    'hidden_units': randint(32, 256),
    'learning_rate': uniform(0.0001, 0.01),
    'dropout_rate': uniform(0, 0.5)
}

from sklearn.model_selection import RandomizedSearchCV

random_search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_dist,
    n_iter=20,
    cv=3,
    random_state=42
)

random_search.fit(x_train, y_train)
print(f"最佳參數: {random_search.best_params_}")
```

## 學習率調優

```python
lr_schedule = keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate=0.001,
    decay_steps=10000,
    decay_rate=0.9
)

optimizer = keras.optimizers.Adam(learning_rate=lr_schedule)

model.compile(
    optimizer=optimizer,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

## 批次大小選擇

批次大小影響：
- 小批次（16-32）：泛化能力較好，震盪較大
- 大批次（128-512）：收斂穩定，可能泛化能力較差

```python
for batch_size in [16, 32, 64, 128]:
    model = create_model()
    model.fit(x_train, y_train, epochs=10, batch_size=batch_size, verbose=0)
    test_acc = model.evaluate(x_test, y_test)[1]
    print(f"Batch size {batch_size}: {test_acc:.2%}")
```

## Keras Tuner

```python
try:
    from kerastuner import Hyperband

    def build_model(hp):
        model = keras.Sequential()
        model.add(layers.Dense(
            hp.Int('units', 32, 512, step=32),
            activation='relu',
            input_shape=(784,)
        ))
        model.add(layers.Dense(10, activation='softmax'))

        model.compile(
            optimizer=keras.optimizers.Adam(
                hp.Float('learning_rate', 1e-4, 1e-2, sampling='log')
            ),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    tuner = Hyperband(
        build_model,
        objective='val_accuracy',
        max_epochs=10,
        directory='my_dir'
    )

    tuner.search(x_train, y_train, epochs=10, validation_split=0.2)
    best_model = tuner.get_best_models(1)[0]
    best_hp = tuner.get_best_hyperparameters(1)[0]
    print(f"最佳 units: {best_hp.get('units')}")
    print(f"最佳 learning_rate: {best_hp.get('learning_rate')}")
except ImportError:
    print("Keras Tuner 未安裝")
```

## 層數與神經元數

```python
architectures = [
    [64],
    [128],
    [64, 32],
    [128, 64],
    [256, 128, 64]
]

for arch in architectures:
    model = keras.Sequential([
        layers.Dense(arch[0], activation='relu', input_shape=(784,))
    ])

    for units in arch[1:]:
        model.add(layers.Dense(units, activation='relu'))

    model.add(layers.Dense(10, activation='softmax'))
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    model.fit(x_train, y_train, epochs=5, verbose=0)

    test_acc = model.evaluate(x_test, y_test, verbose=0)[1]
    print(f"架構 {arch}: {test_acc:.2%}")
```

## 參考資源

- https://www.google.com/search?q=hyperparameter+tuning+neural+network+Python+2019
- https://www.google.com/search?q=learning+rate+batch+size+neural+network+optimization+2019
- https://www.google.com/search?q=Keras+Tuner+hyperband+Random+Search+2019