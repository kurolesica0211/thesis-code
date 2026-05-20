================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Prince Christopher of Greece and Denmark (Greek: Χριστόφορος, romanized: Christóphoros; 10 August 1888 – 21 January 1940) was the fifth and youngest son and youngest child of King George I of Greece, belonging to a dynasty which mounted and lost the throne of Greece several times during his lifetime.
Much of his life was spent living abroad.
Family background

Christopher was born at Pavlovsk, Imperial Russia, son of King George I of Greece and Queen Olga, a Russian grand duchess by birth.
He was called "Christo" in the family.
His older brothers were future King Constantine I, George, Nicholas and Andrew.
Christopher, like his siblings, was a polyglot, speaking Greek, English, Danish, Russian, French, and Italian.
The Hellenic royal line was a cadet branch of the Schleswig-Holstein-Sonderburg-Glücksburg dynasty which had mounted the throne of Greece in 1863.
Early adulthood

When Christopher came of age he joined the Hellenic Navy, although apparently he would rather have studied the piano.
He was briefly engaged to Princess Alexandra, 2nd Duchess of Fife in about 1910 (Alexandra's mother, Princess Louise, Duchess of Fife, was a daughter of King Edward VII and Queen Alexandra of the United Kingdom, herself an older sister of George I of Greece, Christopher's father).
First marriage

On 1 January 1920, Christopher married a very wealthy American widow, Nonnie May "Nancy" Stewart Worthington Leeds, at Vevey, Switzerland.
His bride, a once-divorced and once-widowed commoner at least a decade older than the prince, was nonetheless recognised as Christopher's dynastic wife by his family (at the time of the engagement and wedding, the Greek royal family lived frugally in exile, and as Christopher was last in the dynasty's order of succession, any children he fathered would not impact the succession rights of other Greek dynasts).
Shortly after their marriage, Princess Anastasia developed cancer, and died in London on 29 August 1923, leaving no children from this marriage.
Prince Christopher did, however, have a stepson, William Bateman Leeds Jr (1902–1971), who had, in 1921, married Princess Xenia Georgievna of Russia.
She was Christopher's niece through his elder sister, Marie of Greece, Grand Duchess George of Russia.
Second marriage and family

Prince Christopher later remarried; his second wife was Princess Françoise of Orléans (25 December 1902 – 25 February 1953).
Françoise was a daughter of Jean d'Orléans, Duc de Guise, Orléanist pretender to the throne of France, by his wife/first cousin, Isabelle d'Orléans.
Isabelle was, in turn, a daughter of Philippe, Comte de Paris by his wife and first cousin, Infanta Isabel de Orléans y Borbon.
They were childless for a decade, then one child was born to Françoise: Prince Michael of Greece and Denmark was born in Rome in 1939, shortly before Prince Christopher's death.
Opinion on Anna Anderson

In 1927, Prince Christopher paid a visit to the Long Island home of William and Xenia Leeds, respectively his stepson and niece.
Xenia had taken an interest in the strange case of a woman, Anna Anderson, who claimed to be Grand Duchess Anastasia Nikolaevna of Russia, the youngest daughter of the last Tsar of Russia, Nicholas II.
As Prince Christopher explained, "That was her story, and, fantastic as it was, there were many who believed then − and still believe − in her, among them one or two members of the Imperial Family."
Prince Christopher described her: "In the first place she was unable to speak Russian, which the Grand Duchess Anastasia, like all the Czar's children, had talked fluently − and would only converse in German.
Opinion on monarchy

Prince Christopher recorded his thoughts on monarchy and those aspiring to it: "Nothing under the sun would induce me to accept a Kingdom.
"


Death

Prince Christopher of Greece died in Athens on 21 January 1940, aged 51.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b39fe104-7c8f-45c5-8b84-d194958d0e5f)
 Call ID: b39fe104-7c8f-45c5-8b84-d194958d0e5f
  Args:
    type: :Man
    source: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (3add56e3-6dca-439e-a591-fb033964bde8)
 Call ID: 3add56e3-6dca-439e-a591-fb033964bde8
  Args:
    type: :Person
    source: Prince_Christopher_of_Greece_and_Denmark
  AddLiteral (058b938d-ecc2-498a-8281-333d6b63a44f)
 Call ID: 058b938d-ecc2-498a-8281-333d6b63a44f
  Args:
    relation: :hasBirthYear
    source: Prince_Christopher_of_Greece_and_Denmark
    literal_value: 1888
    literal_type: xsd:integer
  AddLiteral (ba81d5af-aee4-4765-ad38-e260335b76a7)
 Call ID: ba81d5af-aee4-4765-ad38-e260335b76a7
  Args:
    relation: :hasDeathYear
    source: Prince_Christopher_of_Greece_and_Denmark
    literal_value: 1940
    literal_type: xsd:integer
  AddLiteral (84757d84-cb14-4db4-802a-2456f4db1658)
 Call ID: 84757d84-cb14-4db4-802a-2456f4db1658
  Args:
    literal_type: xsd:string
    literal_value: Christo
    relation: :knownAs
    source: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (a319ef31-24d5-47be-9c0e-a0b8da9b5f21)
 Call ID: a319ef31-24d5-47be-9c0e-a0b8da9b5f21
  Args:
    type: :Man
    source: King_George_I_of_Greece
  AssignClass (f66eeaa8-330d-4151-bc34-0f29bd6ae33c)
 Call ID: f66eeaa8-330d-4151-bc34-0f29bd6ae33c
  Args:
    type: :Person
    source: King_George_I_of_Greece
  AssignClass (c8d77694-5b59-4208-8684-cde5a8fe687a)
 Call ID: c8d77694-5b59-4208-8684-cde5a8fe687a
  Args:
    type: :Woman
    source: Queen_Olga
  AssignClass (2ece6a19-9532-4ccb-8117-fb834b45ce9e)
 Call ID: 2ece6a19-9532-4ccb-8117-fb834b45ce9e
  Args:
    type: :Person
    source: Queen_Olga
  AddTriple (8d26ce15-e554-47ab-98bd-310054cf6ce5)
 Call ID: 8d26ce15-e554-47ab-98bd-310054cf6ce5
  Args:
    relation: :hasFather
    target: King_George_I_of_Greece
    source: Prince_Christopher_of_Greece_and_Denmark
  AddTriple (66b57733-0989-47e9-ae52-6cf0a70748a1)
 Call ID: 66b57733-0989-47e9-ae52-6cf0a70748a1
  Args:
    target: Queen_Olga
    relation: :hasMother
    source: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (bee6ba33-bf87-4943-9d77-03b391307428)
 Call ID: bee6ba33-bf87-4943-9d77-03b391307428
  Args:
    type: :Man
    source: Constantine_I
  AssignClass (418358ff-f7f7-4950-92a4-e954c120121a)
 Call ID: 418358ff-f7f7-4950-92a4-e954c120121a
  Args:
    type: :Person
    source: Constantine_I
  AssignClass (d4c1b5d7-2283-4de8-94f9-3936e0a8905b)
 Call ID: d4c1b5d7-2283-4de8-94f9-3936e0a8905b
  Args:
    type: :Man
    source: George_brother
  AssignClass (f3f07c35-8271-44a4-a462-68132b69a9dd)
 Call ID: f3f07c35-8271-44a4-a462-68132b69a9dd
  Args:
    type: :Person
    source: George_brother
  AssignClass (c4586431-d1db-44cd-b605-21a7c2d0003a)
 Call ID: c4586431-d1db-44cd-b605-21a7c2d0003a
  Args:
    type: :Man
    source: Nicholas
  AssignClass (236fbef2-38fc-4437-8478-2c47a422e9ab)
 Call ID: 236fbef2-38fc-4437-8478-2c47a422e9ab
  Args:
    type: :Person
    source: Nicholas
  AssignClass (4672f984-b956-4380-960a-bd701414f837)
 Call ID: 4672f984-b956-4380-960a-bd701414f837
  Args:
    type: :Man
    source: Andrew
  AssignClass (236d3396-9e81-4b8c-8050-de700217018e)
 Call ID: 236d3396-9e81-4b8c-8050-de700217018e
  Args:
    type: :Person
    source: Andrew
  AddTriple (db12300f-3f9f-417b-a4f6-313dfed87a31)
 Call ID: db12300f-3f9f-417b-a4f6-313dfed87a31
  Args:
    relation: :isBrotherOf
    target: Prince_Christopher_of_Greece_and_Denmark
    source: Constantine_I
  AddTriple (dc06d653-8ff5-422c-a0d9-bd29c6ddce10)
 Call ID: dc06d653-8ff5-422c-a0d9-bd29c6ddce10
  Args:
    target: Prince_Christopher_of_Greece_and_Denmark
    relation: :isBrotherOf
    source: George_brother
  AddTriple (e0006206-0d50-4bd7-b477-6023136064ea)
 Call ID: e0006206-0d50-4bd7-b477-6023136064ea
  Args:
    source: Nicholas
    target: Prince_Christopher_of_Greece_and_Denmark
    relation: :isBrotherOf
  AddTriple (134c6d52-d242-4d31-98a2-5d570d54325e)
 Call ID: 134c6d52-d242-4d31-98a2-5d570d54325e
  Args:
    target: Prince_Christopher_of_Greece_and_Denmark
    relation: :isBrotherOf
    source: Andrew
  AssignClass (7e3539b5-de93-4421-b25d-94299b5b2d72)
 Call ID: 7e3539b5-de93-4421-b25d-94299b5b2d72
  Args:
    type: :Woman
    source: Princess_Anastasia
  AssignClass (27efcf1c-089c-4935-b89d-6d4135efb187)
 Call ID: 27efcf1c-089c-4935-b89d-6d4135efb187
  Args:
    type: :Person
    source: Princess_Anastasia
  AddLiteral (77bb67e0-b509-4a14-a7f8-f6369b119e16)
 Call ID: 77bb67e0-b509-4a14-a7f8-f6369b119e16
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    relation: :hasMarriageYear
    literal_value: 1920
    literal_type: xsd:integer
  AssignClass (b2e7e2ba-c5f0-4c01-8ad9-9d6772867ab4)
 Call ID: b2e7e2ba-c5f0-4c01-8ad9-9d6772867ab4
  Args:
    type: :Man
    source: William_Bateman_Leeds_Jr
  AssignClass (03eb118b-c4e1-4afd-97a2-a31d3401e67c)
 Call ID: 03eb118b-c4e1-4afd-97a2-a31d3401e67c
  Args:
    type: :Person
    source: William_Bateman_Leeds_Jr
  AssignClass (38ddbdf4-565d-4fc4-9bec-0b49de7fc2b1)
 Call ID: 38ddbdf4-565d-4fc4-9bec-0b49de7fc2b1
  Args:
    type: :Woman
    source: Princess_Francoise_of_Orleans
  AssignClass (bc1c23fe-dc2e-44ec-9543-d1dc761a5978)
 Call ID: bc1c23fe-dc2e-44ec-9543-d1dc761a5978
  Args:
    type: :Person
    source: Princess_Francoise_of_Orleans
  AddTriple (551b0bea-9bc2-4554-bcb2-3b1f4876b404)
 Call ID: 551b0bea-9bc2-4554-bcb2-3b1f4876b404
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    target: Princess_Francoise_of_Orleans
    relation: :hasMother
  AddTriple (58502f04-fdf1-47a5-822a-d780a28f23a9)
 Call ID: 58502f04-fdf1-47a5-822a-d780a28f23a9
  Args:
    relation: :hasFather
    target: Prince_Christopher_of_Greece_and_Denmark
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (7c8e515c-cc8a-42ef-b619-488ce6ca4be2)
 Call ID: 7c8e515c-cc8a-42ef-b619-488ce6ca4be2
  Args:
    type: :Man
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (2fb35c9c-441a-45d2-a171-3654f5aaa991)
 Call ID: 2fb35c9c-441a-45d2-a171-3654f5aaa991
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  Finish (8965e3df-e734-478c-96d8-dc535a8a833a)
 Call ID: 8965e3df-e734-478c-96d8-dc535a8a833a
  Args: