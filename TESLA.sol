// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TESLA {
    // create the option structure (specifies what elements are needed to define an option)
    struct option {
        uint256 leverage;
        uint256 cap;
        uint256 strike;
        uint256 price;
        uint256 deposit;
        string expiry_str;
        uint256 expiry_int;
        address payable emittent;
        bool available;
        address payable buyer;
        bool expired;
    }

    // create and options array, where all options can be stored and called by their position in the array.
    // The position in the array also serves as the option's unique identifier! (Unless 2**256 options are deployed the number is ensured to be unique)
    option[] public options;

    function createoption(
        uint256 _leverage,
        uint256 _cap,
        uint256 _strike,
        uint256 _priceETH,
        string memory _exp_str,
        uint256 _exp_min
    ) public payable {
        //require payment to cover all potential losses
        require(msg.value >= _leverage * _cap * 10**18);
        //create new option and add it to the option array.
        uint256 _deposit = (_leverage * _cap * 10**18);
        uint256 _priceWEI = _priceETH * 10**18;
        // if string is right create the option, otherwise do nothing.

        uint256 block_exp = block.timestamp + (_exp_min) * (1 minutes);

        //_ strike will be actual strikeprice *100 in order to avoid decimals!!
        options.push(
            option(
                _leverage,
                _cap,
                uint256(_strike),
                _priceWEI,
                _deposit,
                _exp_str,
                block_exp,
                payable(msg.sender),
                true,
                payable(msg.sender),
                false
            )
        );
    }

    function buyoption(uint256 _optionsN) public payable {
        //require payment = price and availability
        require(options[_optionsN].available == true);
        require(options[_optionsN].expired == false);
        require(msg.value == options[_optionsN].price);
        // transfer the payment by the buyer directly to the emittent.
        options[_optionsN].emittent.transfer(msg.value);
        // change options[_optionsN] so that it cannot be bought anymore (available = false) + buyer address.

        options[_optionsN].buyer = payable(msg.sender);
        options[_optionsN].available = false;
    }

    function resolution(uint256 _finalvalue, string memory _alphadate)
        public
        payable
    {
        for (uint256 i = 0; i < options.length; i++) {
            if (
                options[i].expired == false &&
                keccak256(abi.encodePacked(options[i].expiry_str)) ==
                keccak256(abi.encodePacked(_alphadate)) &&
                options[i].expiry_int >= block.timestamp
            ) {
                //determine spread between strike and final value (converted to wei)
                uint256 spread = _finalvalue - options[i].strike;

                //three different cases and modes of payment depending on spread value
                if (options[i].cap > spread) {
                    if (spread <= 0) {
                        options[i].emittent.transfer(options[i].deposit);
                    } else {
                        options[i].buyer.transfer(
                            options[i].leverage * spread * 10**16
                        );
                        options[i].emittent.transfer(
                            options[i].deposit -
                                (options[i].leverage * spread * 10**16)
                        );
                    }
                } else {
                    options[i].buyer.transfer(options[i].deposit);
                }
                options[i].expired = true;
                options[i].available = false;
            } else {}
        }
    }

    function get_length() public view returns (uint256) {
        return (options.length);
    }

    function get_leverage(uint256 _counter) public view returns (uint256) {
        return options[_counter].leverage;
    }

    function get_cap(uint256 _counter) public view returns (uint256) {
        return options[_counter].cap;
    }

    function get_strike(uint256 _counter) public view returns (uint256) {
        return options[_counter].strike;
    }

    function get_price(uint256 _counter) public view returns (uint256) {
        return options[_counter].price;
    }

    function get_emittent(uint256 _counter)
        public
        view
        returns (string memory)
    {
        return string(abi.encodePacked(options[_counter].emittent));
    }

    function get_available(uint256 _counter) public view returns (bool) {
        return (options[_counter].available);
    }

    function get_expirystr(uint256 _counter)
        public
        view
        returns (string memory)
    {
        return (options[_counter].expiry_str);
    }

    function get_expiryint(uint256 _counter) public view returns (uint256) {
        return (options[_counter].expiry_int);
    }

    function get_time() public view returns (uint256) {
        return (block.timestamp);
    }
}
