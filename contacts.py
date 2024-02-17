import Contacts
import objc
import phonenumbers


class Contact:
    def __init__(
        self, first_name: str, last_name: str, phone_numbers: list[str]
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.phone_numbers = phone_numbers

    def __repr__(self) -> str:
        return f"Contact(first_name={self.first_name}, last_name={self.last_name}, phone_numbers={self.phone_numbers})"

    def __str__(self):
        return repr(self)


def get_CNContacts_list() -> list[Contacts.CNContact]:
    """Returns a list of contacts"""
    # Create a contact store

    store = Contacts.CNContactStore.alloc().init()

    # Define keys that you want to fetch (e.g., name)
    keys_to_fetch = [
        Contacts.CNContactGivenNameKey,
        Contacts.CNContactFamilyNameKey,
        Contacts.CNContactPhoneNumbersKey,
    ]

    # Fetch all contacts
    fetch_request = Contacts.CNContactFetchRequest.alloc().initWithKeysToFetch_(
        keys_to_fetch
    )
    error = objc.nil

    # Create an empty list to hold contacts
    contact_list = []

    # Process each contact
    def contact_handler(contact, stop):
        contact_list.append(contact)

    store.enumerateContactsWithFetchRequest_error_usingBlock_(
        fetch_request, error, contact_handler
    )
    return contact_list


def sanitize_phone_num(phone_num: str) -> str:
    """Sanitizes a phone number"""
    try:
        phone_num = bytes(phone_num, "utf-8").decode("utf-8", "ignore")
        phone_num = phone_num.strip().replace(" ", "")
        return phonenumbers.format_number(
            phonenumbers.parse(phone_num, "US"),
            phonenumbers.PhoneNumberFormat.E164,
        )
    except Exception as e:
        print(e, phone_num)


def get_contacts() -> list[Contact]:
    """Returns a list of contacts"""
    contact_list = get_CNContacts_list()
    return list(
        map(
            lambda e: Contact(
                e.givenName(),
                e.familyName(),
                list(
                    map(
                        lambda ea: sanitize_phone_num(str(ea.value().stringValue())),
                        e.phoneNumbers(),
                    )
                ),
            ),
            contact_list,
        )
    )
