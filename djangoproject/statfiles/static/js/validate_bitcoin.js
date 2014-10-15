BigInteger.valueOf = nbv;
BigInteger.prototype.toByteArrayUnsigned = function () {
    var ba = this.toByteArray();
    if (ba.length) {
        if (ba[0] == 0)
            ba = ba.slice(1);
        return ba.map(function (v) {
            return (v < 0) ? v + 256 : v;
        });
    } else
        return ba;
};        
var Bitcoin = {};
(function () {
    var B58 = Bitcoin.Base58 = {
        alphabet: "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz",
        base: BigInteger.valueOf(58),
        decode: function (input) {
            bi = BigInteger.valueOf(0);
            var leadingZerosNum = 0;
            for (var i = input.length - 1; i >= 0; i--) {
                var alphaIndex = B58.alphabet.indexOf(input[i]);
                if (alphaIndex < 0) {
                    throw "Invalid character";
                }
                bi = bi.add(BigInteger.valueOf(alphaIndex)
                .multiply(B58.base.pow(input.length - 1 - i)));
                if (input[i] == "1") leadingZerosNum++;
                else leadingZerosNum = 0;
            }
            var bytes = bi.toByteArrayUnsigned();
            while (leadingZerosNum-- > 0) bytes.unshift(0);
            return bytes;
        }
    };
})();
Bitcoin.Address = function (bytes) {
    if ("string" == typeof bytes)
        bytes = Bitcoin.Address.decodeString(bytes);
    this.hash = bytes;
    this.version = Bitcoin.Address.networkVersion;
};
Bitcoin.Address.networkVersion = 0x00; // mainnet
Bitcoin.Address.decodeString = function (string) {
    var bytes = Bitcoin.Base58.decode(string);
    var hash = bytes.slice(0, 21);
    var checksum = Crypto.SHA256(Crypto.SHA256(hash, { asBytes: true }), { asBytes: true });
    if (checksum[0] != bytes[21] ||
        checksum[1] != bytes[22] ||
        checksum[2] != bytes[23] ||
        checksum[3] != bytes[24])
        throw "Checksum validation failed!";
    var version = hash.shift();
    if (version != 0)
        throw "Version " + version + " not supported!";
    return hash;
};
function check_address(address) {
    try {
        Bitcoin.Address(address);
        return true;
    } catch (err) {
        return false;
    }
}
