## React Select
React Select documentation: https://react-select.com/home

Some child elements of the React-Select container exist only when the 
drop-down is expanded. This makes debugging via a Browser's dev tools 
difficult because the drop-down will collapse when trying to view
its contents.

Drop-Down not expanded. Menu `<div>` does not exist.
```HTML
<!-- CONTAINER -->
<div class=" css-2b097c-container">
    <!-- CONTROL -->
    <div class=" css-yk16xz-control">
        <!-- VALUES -->
        <div class=" css-gld714-ValueContainer">
            <div class=" css-1wa3eu0-placeholder">Select...</div>
            <!-- INPUT CONTAINER -->
            <div class="css-b8ldur-Input">
                <div class=style"display: inline-block;">
                    <input id="react-select-3-input">
                    <div></div>
                </div>
            </div>
        </div>
        <!-- INDICATOR -->
        <div class=" css-1hb7zxy-IndicatorsContainer">
            <span class=" css-1okebmr-indicatorSeparator"></span>
            <div aria-hidden="true" class=" css-tlfecz-indicatorContainer">
                <svg class="css-6q0nyr-Svg"></svg>
            </div>
        </div>
    </div>
</div>
```

Drop-Down expanded. Menu `<div>` exists.
```HTML
<!-- CONTAINER -->
<div class=" css-2b097c-container">
    <span aria-live="polite" class="css-11aao21-a11yText">
        <p id="aria-selection-event">&nbsp;</p>
        <p id="aria-context">&nbsp;  some text
    </span>
    <!-- CONTROL -->
    <div class=" css-1pahdxg-control">
        <!-- VALUES -->
        <div class=" css-gld714-ValueContainer">
            <div class=" css-1wa3eu0-placeholder">Select...</div>
            <!-- INPUT CONTAINER -->
            <div class="css-b8ldur-Input">
                <div class=style"display: inline-block;">
                    <input id="react-select-3-input">
                    <div></div>
                </div>
            </div>
        </div>
        <!-- INDICATOR -->
        <div class=" css-1hb7zxy-IndicatorsContainer">
            <span class=" css-1okebmr-indicatorSeparator"></span>
            <div aria-hidden="true" class=" css-tlfecz-indicatorContainer">
                <svg class="css-6q0nyr-Svg"></svg>
            </div>
        </div>
    </div>
    <!-- MENU -->
    <div class=" css-26l3qy-menu">
        <div>
            <div>
                label1
            </div>
            <div>
                label2
            </div>
            <div>
                label3
            </div>
        </div>
    </div>
</div>
```