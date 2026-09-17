import streamlit as st
import re
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Tiny Generative AI model by dense Neural Network", layout="wide")

if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

st.title("Tiny Generative AI model by dense Neural Network")

# 1. Mermaid Diagrams and Explanations
st.header("Overview")
st.markdown("### 1. Data Pipeline Flow")
st.components.v1.html("""
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({ startOnLoad: true });
    </script>
    <div class="mermaid">
    graph TD;
        A[Raw Text] --> B[Tokenize & Preprocess];
        B --> C[Create Bigrams Ch1 --> Ch2];
        C --> D[Count Frequencies Tensor N];
        D --> E[Convert to Probabilities P];
    </div>
    """, height=300)

st.markdown("### 2. Neural Network Flow")
st.components.v1.html("""
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({ startOnLoad: true });
    </script>
    <div class="mermaid">
    graph TD;
        A[Input Character] --> B[Encoder string to integer stoi];
        B --> C[One-Hot Encoding xenc];
        C --> D[Dense Linear Layer Weights W];
        D --> E[Logits];
        E --> F[Softmax to Probabilities Decoder];
        F --> G[Sample Next Character itos];
    </div>
    """, height=400)

st.markdown("""
### Encoder, Decoder, and Output Generation

**Encoder**: 
The encoder maps characters to a numerical representation the neural network can understand. We create a dictionary `stoi` (String to Integer) that assigns an integer index to each unique character in our dataset (including a special token `.` for start/end). For a neural network, this index is further transformed into a **one-hot encoded tensor** `xenc` of size `(N, 27)` (assuming 27 unique tokens). A one-hot vector is all zeros except for a `1` at the index corresponding to the character.

**Decoder and Logits**: 
The neural network outputs what are called **logits**. In this context, logits are raw, unnormalized scores that the network assigns to each possible next character. You can think of them as "log-counts" indicating how strongly the network believes a particular character should come next. Because logits can be positive, negative, or zero, they aren't directly usable as probabilities. 

To convert logits into a valid probability distribution (where all numbers are positive and sum to 1), we apply a **Softmax-like** operation:
1. **Exponentiation (`logits.exp()`)**: We take the exponential of every logit. This makes all values positive and exaggerates the differences between high and low scores. This is equivalent to converting the "log-counts" back into raw "counts".
2. **Normalization**: We divide each exponentiated value by the sum of all values. This ensures the final array sums perfectly to 1.0, giving us valid probabilities.

Finally, we use the inverse mapping `itos` (Integer to String) to convert the sampled numerical index back into a readable character.

**Output Array & Generation**:
The output of our neural network for a single character input is a 1D probability array (or tensor) of size `27` (representing the 27 possible next characters). 
To generate text, we:
1. Start with the special token `.` (index 0).
2. Feed it into the model to get the 27-element probability array.
3. Use `torch.multinomial` to randomly sample an index from this distribution.
4. Convert the sampled index to a character and append it to our output.
5. Feed this new character back into the model to predict the next one.
6. Stop when the model generates the `.` token again.
""")

st.divider()

# STEP 1
if st.session_state.current_step >= 1:
    st.header("Step 1: Load Data")
    st.code("words = open('Brands.txt', 'r', encoding='utf-8').read().splitlines()", language='python')
    if st.session_state.current_step == 1:
        if st.button("Run Step 1"):
            try:
                words = open('Brands.txt', 'r', encoding='utf-8').read().splitlines()
                st.session_state.words = words
                st.session_state.current_step = 2
                st.rerun()
            except FileNotFoundError:
                st.error("Brands.txt not found.")
    else:
        st.success(f"Loaded {len(st.session_state.words)} words.")

# STEP 2
if st.session_state.current_step >= 2:
    st.header("Step 2: Preprocess Words")
    st.code('''words = [w.lower() for w in words if len(w) > 0]
words = [re.sub(r"[^a-z]+", '', w) for w in words]''', language='python')
    if st.session_state.current_step == 2:
        if st.button("Run Step 2"):
            words = [w.lower() for w in st.session_state.words if len(w) > 0]
            words = [re.sub(r"[^a-z]+", '', w) for w in words]
            st.session_state.words = words
            st.session_state.current_step = 3
            st.rerun()
    else:
        st.success(f"Number of words after preprocessing: {len(st.session_state.words)}")

# STEP 3
if st.session_state.current_step >= 3:
    st.header("Step 3: Setup Vocabulary and Tensors")
    st.code('''import torch
chars = sorted(list(set(''.join(words))))
stoi = {s:i+1 for i,s in enumerate(chars)}
stoi['.'] = 0
itos = {i:s for s,i in stoi.items()}
N = torch.zeros((27, 27), dtype=torch.int32)

for w in words:
  chs = ['.'] + list(w) + ['.']
  for ch1, ch2 in zip(chs, chs[1:]):
    ix1 = stoi[ch1]
    ix2 = stoi[ch2]
    N[ix1, ix2] += 1''', language='python')
    if st.session_state.current_step == 3:
        if st.button("Run Step 3"):
            words = st.session_state.words
            chars = sorted(list(set(''.join(words))))
            stoi = {s:i+1 for i,s in enumerate(chars)}
            stoi['.'] = 0
            itos = {i:s for s,i in stoi.items()}
            N = torch.zeros((27, 27), dtype=torch.int32)
            for w in words:
              chs = ['.'] + list(w) + ['.']
              for ch1, ch2 in zip(chs, chs[1:]):
                ix1 = stoi[ch1]
                ix2 = stoi[ch2]
                N[ix1, ix2] += 1
            st.session_state.stoi = stoi
            st.session_state.itos = itos
            st.session_state.N = N
            st.session_state.current_step = 4
            st.rerun()
    else:
        st.success("Vocabulary and Tensor N populated.")
        fig = plt.figure(figsize=(12,12))
        plt.imshow(st.session_state.N, cmap='Blues')
        for i in range(27):
            for j in range(27):
                chstr = st.session_state.itos[i] + st.session_state.itos[j]
                plt.text(j, i, chstr, ha="center", va="bottom", color='gray')
                plt.text(j, i, st.session_state.N[i, j].item(), ha="center", va="top", color='gray')
        plt.axis('off')
        st.pyplot(fig)

# STEP 4
if st.session_state.current_step >= 4:
    st.header("Step 4: Explicit Bigram Probability (Counts)")
    st.code('''P = (N+1).float()
P /= P.sum(1, keepdims=True)''', language='python')
    if st.session_state.current_step == 4:
        if st.button("Run Step 4"):
            N = st.session_state.N
            P = (N+1).float()
            P /= P.sum(1, keepdims=True)
            st.session_state.P = P
            st.session_state.current_step = 5
            st.rerun()
    else:
        st.success(f"Probabilities P calculated. Shape: {st.session_state.P.shape}")

# STEP 5
if st.session_state.current_step >= 5:
    st.header("Step 5: Create Neural Net Dataset")
    st.code('''xs, ys = [], []
for w in words:
  chs = ['.'] + list(w) + ['.']
  for ch1, ch2 in zip(chs, chs[1:]):
    ix1 = stoi[ch1]
    ix2 = stoi[ch2]
    xs.append(ix1)
    ys.append(ix2)
xs = torch.tensor(xs)
ys = torch.tensor(ys)''', language='python')
    if st.session_state.current_step == 5:
        if st.button("Run Step 5"):
            xs, ys = [], []
            for w in st.session_state.words:
              chs = ['.'] + list(w) + ['.']
              for ch1, ch2 in zip(chs, chs[1:]):
                ix1 = st.session_state.stoi[ch1]
                ix2 = st.session_state.stoi[ch2]
                xs.append(ix1)
                ys.append(ix2)
            st.session_state.xs = torch.tensor(xs)
            st.session_state.ys = torch.tensor(ys)
            st.session_state.current_step = 6
            st.rerun()
    else:
        st.success(f"Dataset created with {st.session_state.xs.nelement()} examples.")

# STEP 6
if st.session_state.current_step >= 6:
    st.header("Step 6: Train Dense Neural Network")
    st.code('''g = torch.Generator().manual_seed(2147483647)
W = torch.randn((27, 27), generator=g, requires_grad=True)
xenc = F.one_hot(xs, num_classes=27).float()

for k in range(100):
  logits = xenc @ W
  counts = logits.exp()
  probs = counts / counts.sum(1, keepdims=True)
  loss = -probs[torch.arange(num), ys].log().mean() + 0.01*(W**2).mean()
  
  W.grad = None
  loss.backward()
  W.data += -50 * W.grad''', language='python')
    if st.session_state.current_step == 6:
        if st.button("Run Step 6 (Train Model)"):
            xs = st.session_state.xs
            ys = st.session_state.ys
            num = xs.nelement()
            g = torch.Generator().manual_seed(2147483647)
            W = torch.randn((27, 27), generator=g, requires_grad=True)
            xenc = F.one_hot(xs, num_classes=27).float()
            
            losses = []
            for k in range(100):
                logits = xenc @ W
                counts = logits.exp()
                probs = counts / counts.sum(1, keepdims=True)
                loss = -probs[torch.arange(num), ys].log().mean() + 0.01*(W**2).mean()
                losses.append(loss.item())

                W.grad = None
                loss.backward()
                W.data += -50 * W.grad
                
            st.session_state.W = W
            st.session_state.losses = losses
            st.session_state.current_step = 7
            st.rerun()
    else:
        st.success(f"Training complete. Final loss: {st.session_state.losses[-1]}")
        st.line_chart(st.session_state.losses, width=700)

# STEP 7
if st.session_state.current_step >= 7:
    st.header("Step 7: Sample & Generate Text from Neural Net")
    st.code('''g = torch.Generator().manual_seed(2147483647)
for i in range(5):
  out = []
  ix = 0
  while True:
    xenc = F.one_hot(torch.tensor([ix]), num_classes=27).float()
    logits = xenc @ W
    counts = logits.exp()
    p = counts / counts.sum(1, keepdims=True)

    ix = torch.multinomial(p, num_samples=1, replacement=True, generator=g).item()
    out.append(itos[ix])
    if ix == 0:
      break
  print(''.join(out))''', language='python')
    if st.session_state.current_step == 7:
        if st.button("Run Step 7 (Generate)"):
            g = torch.Generator().manual_seed(2147483647)
            W = st.session_state.W
            itos = st.session_state.itos
            sampled_nn = []
            for i in range(5):
              out = []
              ix = 0
              while True:
                xenc_sample = F.one_hot(torch.tensor([ix]), num_classes=27).float()
                logits = xenc_sample @ W
                counts = logits.exp()
                p = counts / counts.sum(1, keepdims=True)

                ix = torch.multinomial(p, num_samples=1, replacement=True, generator=g).item()
                out.append(itos[ix])
                if ix == 0:
                  break
              sampled_nn.append(''.join(out))
            st.session_state.sampled_nn = sampled_nn
            st.session_state.current_step = 8
            st.rerun()
    else:
        st.success("Text Generated:")
        for w in st.session_state.sampled_nn:
            st.write(f"- {w}")

# STEP 8
if st.session_state.current_step >= 8:
    st.header("Step 8: Predict Next Character")
    input_char = st.text_input("Enter a single character (a-z or '.'):", "a").lower()
    
    if st.button("Predict Next Character"):
        if len(input_char) != 1 or input_char not in st.session_state.stoi:
            st.error("Please enter a single valid character from a-z or '.'.")
        else:
            g = torch.Generator().manual_seed(2147483647)
            W = st.session_state.W
            itos = st.session_state.itos
            stoi = st.session_state.stoi
            
            ix = stoi[input_char]
            xenc_sample = F.one_hot(torch.tensor([ix]), num_classes=27).float()
            logits = xenc_sample @ W
            counts = logits.exp()
            p = counts / counts.sum(1, keepdims=True)
            
            next_ix = torch.multinomial(p, num_samples=1, replacement=True, generator=g).item()
            next_char = itos[next_ix]
            
            st.success(f"Given input **'{input_char}'**, the next predicted character is **'{next_char}'**")
            
            import pandas as pd
            st.write(f"### Probabilities for '{input_char}'")
            prob_row = p.detach().numpy()
            prob_df = pd.DataFrame(prob_row, columns=list(stoi.keys()), index=[input_char])
            st.dataframe(prob_df)
