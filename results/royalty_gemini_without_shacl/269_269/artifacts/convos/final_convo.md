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
Lord Frederick Michael George David Louis Windsor (born 6 April 1979) is a member of the British royal family.
He is the only son of Prince and Princess Michael of Kent, and is 54th in the line of succession to the British throne.
He is married to British actress Sophie Winkleman and is a financial analyst by profession.
As a great-grandchild of King George V and Queen Mary, he is a second cousin of King Charles III.
Early life and education

Frederick Michael George David Louis Windsor was born on 6 April 1979 at St Mary's Hospital, London, and was christened on 11 July at the Chapel Royal, St James's Palace, Westminster.
A first cousin once removed of Queen Elizabeth II and a first cousin twice removed of Prince Philip, Duke of Edinburgh, he is therefore both a second cousin and a second cousin once removed of King Charles III and his siblings.
Frederick and his sister, Lady Gabriella, were brought up in the Church of England.
Career

After graduating, Frederick worked as a fashion model, appearing in a campaign for Burberry and for the designer Tomasz Starzewski, and also as a music journalist, notably for Tatler magazine.
Personal life

On St Valentine's Day, 14 February 2009, Frederick became engaged to the actress Sophie Winkleman.
She was baptised at St James's Palace in December 2013 and has Princess Eugenie among her godparents.
Maud served as a bridesmaid at the wedding of Princess Eugenie and Jack Brooksbank in 2018.
On 20 January 2016, it was announced Frederick and Sophie had become parents to a second daughter, Isabella Alexandra May, who was born on 16 January 2016 at Chelsea and Westminster Hospital in London.
From September 2016 until its closure in 2023, Frederick was president of the charity Soldier On!, which supported vulnerable, disadvantaged, or socially isolated people through archaeology and heritage projects as well as personal development workshops.
On 21 February 2017, Frederick was inducted into the Grand Order of Water Rats charitable fraternity.
Titles and styles

Under letters patent issued in 1917 and still in force today, Frederick's father is entitled to the dignity of prince and the style His Royal Highness as the son of a son of George V. Although these letters do not bestow these royal dignities beyond grandchildren of monarchs (except in the case of the children of the Prince of Wales, as modified by Elizabeth II), they allow the children of sons of sons of a British monarch to be styled as the children of a duke, with the honorific courtesy style of Lord or Lady before their given names.
Since Lord Frederick is not a peer in his own right, his style is not hereditary and his children are not entitled to any distinctions, including the prefix The Honourable.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (a212346a-0ac1-4848-a8a8-feb6c221155a)
 Call ID: a212346a-0ac1-4848-a8a8-feb6c221155a
  Args:
    source: :Lord_Frederick_Windsor
    type: :Man
  AssignClass (7ea3db2e-d821-406c-8d55-3aca340363de)
 Call ID: 7ea3db2e-d821-406c-8d55-3aca340363de
  Args:
    source: :Lord_Frederick_Windsor
    type: :Person
  AddLiteral (47ffe69b-0325-46ab-84be-6a9261e2d776)
 Call ID: 47ffe69b-0325-46ab-84be-6a9261e2d776
  Args:
    relation: :hasBirthYear
    literal_value: 1979
    source: :Lord_Frederick_Windsor
    literal_type: xsd:integer
  AssignClass (ca6c85e8-3a83-42d8-8aa4-09a76230bd80)
 Call ID: ca6c85e8-3a83-42d8-8aa4-09a76230bd80
  Args:
    type: :Man
    source: :Prince_Michael_of_Kent
  AssignClass (835e4824-50cd-4240-b295-af08afd68e18)
 Call ID: 835e4824-50cd-4240-b295-af08afd68e18
  Args:
    type: :Person
    source: :Prince_Michael_of_Kent
  AssignClass (8061e39a-08c6-49f8-bb0a-de7dac8bdc43)
 Call ID: 8061e39a-08c6-49f8-bb0a-de7dac8bdc43
  Args:
    type: :Woman
    source: :Princess_Michael_of_Kent
  AssignClass (dece96bd-9ee1-4a66-9ac5-c5e5dc424a1f)
 Call ID: dece96bd-9ee1-4a66-9ac5-c5e5dc424a1f
  Args:
    source: :Princess_Michael_of_Kent
    type: :Person
  AddTriple (351c4575-e4fa-444c-a3f5-3520ba79058f)
 Call ID: 351c4575-e4fa-444c-a3f5-3520ba79058f
  Args:
    relation: :hasFather
    source: :Lord_Frederick_Windsor
    target: :Prince_Michael_of_Kent
  AddTriple (4790a59c-291e-41b4-896c-015cadeec00e)
 Call ID: 4790a59c-291e-41b4-896c-015cadeec00e
  Args:
    relation: :hasMother
    target: :Princess_Michael_of_Kent
    source: :Lord_Frederick_Windsor
  AssignClass (1b87e45a-46f1-4a12-9422-b72a84cc9a2f)
 Call ID: 1b87e45a-46f1-4a12-9422-b72a84cc9a2f
  Args:
    source: :Sophie_Winkleman
    type: :Woman
  AssignClass (d7d9edf4-c75e-4682-97c4-8bba6dc39809)
 Call ID: d7d9edf4-c75e-4682-97c4-8bba6dc39809
  Args:
    source: :Sophie_Winkleman
    type: :Person
  AddLiteral (45f37116-5c22-4db1-8bff-b3e1890882e7)
 Call ID: 45f37116-5c22-4db1-8bff-b3e1890882e7
  Args:
    literal_type: xsd:integer
    source: :Lord_Frederick_Windsor
    literal_value: 2009
    relation: :hasMarriageYear
  AddTriple (0e430ece-99fb-4064-8b87-10bc702ffd26)
 Call ID: 0e430ece-99fb-4064-8b87-10bc702ffd26
  Args:
    relation: :hasRelation
    target: :Sophie_Winkleman
    source: :Lord_Frederick_Windsor
  AssignClass (36343847-462d-4a03-ba96-298fd4573617)
 Call ID: 36343847-462d-4a03-ba96-298fd4573617
  Args:
    source: :Lady_Gabriella
    type: :Woman
  AssignClass (60ea282a-281e-40c7-a858-7ac9751ca1dd)
 Call ID: 60ea282a-281e-40c7-a858-7ac9751ca1dd
  Args:
    type: :Person
    source: :Lady_Gabriella
  AddTriple (2e8c6d8f-86c8-4e4f-945a-ab952e8b9e73)
 Call ID: 2e8c6d8f-86c8-4e4f-945a-ab952e8b9e73
  Args:
    relation: :isSiblingOf
    target: :Lady_Gabriella
    source: :Lord_Frederick_Windsor
  AssignClass (8f8e1c75-dca9-4814-beb3-814b22daf315)
 Call ID: 8f8e1c75-dca9-4814-beb3-814b22daf315
  Args:
    source: :Isabella_Alexandra_May
    type: :Woman
  AssignClass (426de005-5514-400c-94b1-bc6caced244e)
 Call ID: 426de005-5514-400c-94b1-bc6caced244e
  Args:
    source: :Isabella_Alexandra_May
    type: :Person
  AddTriple (9346273d-3520-45a7-9012-ff007a7f8887)
 Call ID: 9346273d-3520-45a7-9012-ff007a7f8887
  Args:
    relation: :isDaughterOf
    target: :Lord_Frederick_Windsor
    source: :Isabella_Alexandra_May
  AddTriple (5aa41b6e-3c2d-4347-85f2-63a088b8acd8)
 Call ID: 5aa41b6e-3c2d-4347-85f2-63a088b8acd8
  Args:
    source: :Isabella_Alexandra_May
    target: :Sophie_Winkleman
    relation: :isDaughterOf
  AssignClass (10ab657c-5949-43b2-b509-db87d75b75ae)
 Call ID: 10ab657c-5949-43b2-b509-db87d75b75ae
  Args:
    type: :Man
    source: :King_George_V
  AssignClass (a2c8ac04-a83a-4352-a7a4-8356e849a5d5)
 Call ID: a2c8ac04-a83a-4352-a7a4-8356e849a5d5
  Args:
    type: :Person
    source: :King_George_V
  AssignClass (2018537a-abf2-4942-b290-a3772dabd9e7)
 Call ID: 2018537a-abf2-4942-b290-a3772dabd9e7
  Args:
    source: :Queen_Mary
    type: :Woman
  AssignClass (a99f1b78-3d4c-4a3c-841b-5b22b81cfd17)
 Call ID: a99f1b78-3d4c-4a3c-841b-5b22b81cfd17
  Args:
    source: :Queen_Mary
    type: :Person
  AddTriple (2c7232d2-de50-43f5-b4a8-9ccd147b171c)
 Call ID: 2c7232d2-de50-43f5-b4a8-9ccd147b171c
  Args:
    target: :Lord_Frederick_Windsor
    source: :King_George_V
    relation: :isAncestorOf
  AddTriple (e9cde61b-cb90-4f01-9c90-640e68b3cf41)
 Call ID: e9cde61b-cb90-4f01-9c90-640e68b3cf41
  Args:
    relation: :isAncestorOf
    target: :Lord_Frederick_Windsor
    source: :Queen_Mary
  Finish (bb30f81c-1313-4712-9c2b-db7324be802f)
 Call ID: bb30f81c-1313-4712-9c2b-db7324be802f
  Args: