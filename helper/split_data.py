from dataclass import Dataclass
from sklearn.model_selection import train_test_split

def split_data(
        data, 
        target_name,
        train_rows,
        valid_rows,
        random_state,
        shuffle,
        stratify
        ):
    X = data.drop(target_name, axis=1)
    y = data[target_name]
    train_X, valid_X, train_y,  valid_y = train_test_split(
        X, 
        y, 
        train_size=train_rows, 
        test_size=valid_rows, 
        random_state=random_state,
        shuffle=shuffle,
        stratify=data[stratify] if stratify is not None else None
        )

    # Add datasets to the session
    Dataclass.SESSION['train_X'] = train_X
    Dataclass.SESSION['valid_X'] = valid_X
    Dataclass.SESSION['train_y'] = train_y
    Dataclass.SESSION['valid_y'] = valid_y

    # Add the name of the target variable
    Dataclass.SESSION['target_name'] = target_name

    return (train_X, train_y, valid_X, valid_y)