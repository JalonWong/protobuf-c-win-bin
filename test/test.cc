#include <gtest/gtest.h>
#include <test/test.pb-c.h>

TEST(PROTOBUF_C, TEST1) {
    Foo__Person__PhoneNumber__Comment comment = FOO__PERSON__PHONE_NUMBER__COMMENT__INIT;
    Foo__Person__PhoneNumber phone = FOO__PERSON__PHONE_NUMBER__INIT;
    Foo__Person__PhoneNumber *phone_numbers[1];
    Foo__Person person = FOO__PERSON__INIT;
    Foo__Person *person2;
    unsigned char simple_pad[8];
    size_t size, size2;
    unsigned char *packed;
    ProtobufCBufferSimple bs = PROTOBUF_C_BUFFER_SIMPLE_INIT (simple_pad);

    comment.comment = (char*)"protobuf-c guy";

    phone.number = (char*)"1234";
    phone.type = FOO__PERSON__PHONE_TYPE__WORK;
    phone.comment = &comment;

    phone_numbers[0] = &phone;

    person.name = (char*)"dave b";
    person.id = 42;
    person.n_phone = 1;
    person.phone = phone_numbers;

    size = foo__person__get_packed_size (&person);
    packed = (unsigned char *)malloc (size);
    ASSERT_TRUE(packed != NULL);

    size2 = foo__person__pack (&person, packed);

    ASSERT_TRUE(size == size2);
    foo__person__pack_to_buffer (&person, &bs.base);
    ASSERT_TRUE(bs.len == size);
    ASSERT_TRUE(memcmp (bs.data, packed, size) == 0);

    PROTOBUF_C_BUFFER_SIMPLE_CLEAR (&bs);

    person2 = foo__person__unpack (NULL, size, packed);
    ASSERT_TRUE(person2 != NULL);
    ASSERT_TRUE(person2->id == 42);
    ASSERT_TRUE(strcmp (person2->email, "") == 0);
    ASSERT_TRUE(strcmp (person2->name, "dave b") == 0);
    ASSERT_TRUE(person2->n_phone == 1);
    ASSERT_TRUE(strcmp (person2->phone[0]->number, "1234") == 0);
    ASSERT_TRUE(person2->phone[0]->type == FOO__PERSON__PHONE_TYPE__WORK);
    ASSERT_TRUE(strcmp (person2->phone[0]->comment->comment, "protobuf-c guy") == 0);

    foo__person__free_unpacked (person2, NULL);
    free (packed);
}
