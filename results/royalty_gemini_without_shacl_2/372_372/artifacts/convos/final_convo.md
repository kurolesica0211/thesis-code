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
Prince George William of Hanover and Cumberland (Georg Wilhelm Ernst August Friedrich Axel Prinz von Hannover; 25 March 1915 – 8 January 2006) was the second-eldest son of Ernest Augustus, Duke of Brunswick, and his wife Princess Victoria Louise of Prussia, the only daughter of Wilhelm II, German Emperor, and Augusta Victoria of Schleswig-Holstein.
George William's wife was a sister of Prince Philip, Duke of Edinburgh, and his children are thus first cousins of King Charles III.
His sister, Frederica, became Queen of the Hellenes as the consort of King Paul of Greece.
He held the title of Prince of the United Kingdom of Great Britain and Ireland, granted ad personam to the children of the then-Duke of Brunswick by George V's letters patent of 1914, which remained unrevoked.
Life

George William was christened on 10 May 1915 in Brunswick.
The prince's godparents included Maria Christina of Austria, Prince Axel of Denmark, and Princess Olga of Hanover and Cumberland who held the infant prince over the baptismal font.
From 1930 through 1934, Prince George William attended the elite boarding school Schule Schloss Salem in Überlingen on Lake Constance.
Schule Schloss Salem was co-founded by the prince's uncle, the last Chancellor of the German Empire, Prince Maximilian of Baden, and educator Kurt Hahn in 1920.
A former student of the institution, the prince then went to Scotland with his wife to meet with Kurt Hahn, the founder of the school, and to visit Gordonstoun, the establishment that the latter founded when he had to flee Nazi Germany because of his Jewish origins.
Together with his wife, as well as his three brothers, he took part in the ship tours organized by his sister Queen Frederica and her husband King Paul of Greece in 1954 and 1956, which became known as the “Cruises of the Kings” and were attended by over 100 royals from all over Europe.
For many years Prince George William was a member of the International Olympic Committee (IOC) and of the Deutscher Olympischer Sportbund (DOSB), the German NOC.
Prince George William of Hanover lived in Schliersee, near Munich, and died in Munich in 2006 aged 90.
His wife, Sophie, sister of Prince Philip of Greece and Denmark, later Duke of Edinburgh, consort of Queen Elizabeth II of the United Kingdom, died in 2001.
Marriage

On 23 April 1946 in Salem, Baden-Württemberg, Germany, Prince George William married his third cousin Princess Sophie of Greece and Denmark, daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, and the widow of Prince Christoph of Hesse.
After consultations with the Foreign Office, Home Office and King George VI's private secretary, Sir Alan Lascelles, a ciphered telegram dated 18 April 1946 and crafted by Sir Albert Napier, permanent secretary to the Lord Chancellor, was transmitted from the British Foreign Office to the Foreign Adviser to the British Commander in Chief at Berlin:


"The Duke of Brunswick has formally applied to The King by letter of March 22nd for the consent of His Majesty under the Act 12 Geo.
11 to the marriage of his son Prince George William with Princess Sophia Dowager Princess of Hesse.
Please convey to the Duke an informal intimation that in view of the fact that a state of war still exists between Great Britain and Germany, His Majesty is advised that the case is not one in which it is practicable for His consent to be given in the manner contemplated by the Act.
"

They had three children: Welf (1947–1981), Georg (born 1949) and Friederike (born 1954).
Ancestry

George William was a descendant of Victoria of the United Kingdom and Albert, Prince Consort through their eldest daughter Victoria, Princess Royal, the wife of Frederick III, German Emperor.
He was born a Prince of the United Kingdom of Great Britain and Ireland.



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
  AssignClass (a19f7e84-c02d-4bce-a63f-79c7857ff1bf)
 Call ID: a19f7e84-c02d-4bce-a63f-79c7857ff1bf
  Args:
    source: George_William_of_Hanover_and_Cumberland
    type: :Man
  AddLiteral (c11a2a90-5184-4c03-a1a1-8a0a16c98bed)
 Call ID: c11a2a90-5184-4c03-a1a1-8a0a16c98bed
  Args:
    relation: :hasBirthYear
    literal_value: 1915
    literal_type: xsd:positiveInteger
    source: George_William_of_Hanover_and_Cumberland
  AddLiteral (b571289b-9643-48cd-8e8b-f5f2dfe0f4b3)
 Call ID: b571289b-9643-48cd-8e8b-f5f2dfe0f4b3
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 2006
    source: George_William_of_Hanover_and_Cumberland
    relation: :hasDeathYear
  AssignClass (0ef53893-1c7c-4350-8d43-c4326e73a1c4)
 Call ID: 0ef53893-1c7c-4350-8d43-c4326e73a1c4
  Args:
    type: :Man
    source: Ernest_Augustus_Duke_of_Brunswick
  AssignClass (bb540d2b-bd45-48ce-a6fe-fe9ba0334996)
 Call ID: bb540d2b-bd45-48ce-a6fe-fe9ba0334996
  Args:
    type: :Woman
    source: Victoria_Louise_of_Prussia
  AddTriple (c7e68320-20ea-4636-9b20-a4d3e9634d8e)
 Call ID: c7e68320-20ea-4636-9b20-a4d3e9634d8e
  Args:
    source: George_William_of_Hanover_and_Cumberland
    relation: :hasFather
    target: Ernest_Augustus_Duke_of_Brunswick
  AddTriple (42593c55-c7e0-4415-b40f-ec2f8d464613)
 Call ID: 42593c55-c7e0-4415-b40f-ec2f8d464613
  Args:
    source: George_William_of_Hanover_and_Cumberland
    relation: :hasMother
    target: Victoria_Louise_of_Prussia
  AssignClass (2d26493b-6b90-4b54-a5bb-68ebd92203ca)
 Call ID: 2d26493b-6b90-4b54-a5bb-68ebd92203ca
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AssignClass (1bc10858-a6df-4778-ab7c-5671a69d1cf0)
 Call ID: 1bc10858-a6df-4778-ab7c-5671a69d1cf0
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Woman
  AddTriple (c6929ff2-4993-4210-8e14-3576a2cd0c5a)
 Call ID: c6929ff2-4993-4210-8e14-3576a2cd0c5a
  Args:
    target: Wilhelm_II_German_Emperor
    relation: :hasFather
    source: Victoria_Louise_of_Prussia
  AddTriple (27045ad7-ecb2-49cf-a234-46845b735cb2)
 Call ID: 27045ad7-ecb2-49cf-a234-46845b735cb2
  Args:
    target: Augusta_Victoria_of_Schleswig-Holstein
    relation: :hasMother
    source: Victoria_Louise_of_Prussia
  AssignClass (a9f54d5b-ed18-4fec-84b2-7e3bfd253f78)
 Call ID: a9f54d5b-ed18-4fec-84b2-7e3bfd253f78
  Args:
    source: Sophie_of_Greece_and_Denmark
    type: :Woman
  AddTriple (c6379434-26a1-4e20-911f-d7bc8020887c)
 Call ID: c6379434-26a1-4e20-911f-d7bc8020887c
  Args:
    source: George_William_of_Hanover_and_Cumberland
    relation: :hasRelation
    target: Sophie_of_Greece_and_Denmark
  AddLiteral (cdb762dc-7121-41cb-b3ea-a34123ae3e6f)
 Call ID: cdb762dc-7121-41cb-b3ea-a34123ae3e6f
  Args:
    relation: :hasMarriageYear
    source: George_William_of_Hanover_and_Cumberland
    literal_type: xsd:positiveInteger
    literal_value: 1946
  AddLiteral (3b81a031-5c10-411f-b97b-a013efb509ec)
 Call ID: 3b81a031-5c10-411f-b97b-a013efb509ec
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 2001
    source: Sophie_of_Greece_and_Denmark
    relation: :hasDeathYear
  AssignClass (d7bc9937-93d5-4773-91ce-41d00ca4a20b)
 Call ID: d7bc9937-93d5-4773-91ce-41d00ca4a20b
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AddTriple (a4912913-62cd-4d47-a204-fb308158286a)
 Call ID: a4912913-62cd-4d47-a204-fb308158286a
  Args:
    target: Prince_Philip_Duke_of_Edinburgh
    relation: :isSiblingOf
    source: Sophie_of_Greece_and_Denmark
  AssignClass (6f6a0661-da1f-4499-b61f-6909bc2bfc10)
 Call ID: 6f6a0661-da1f-4499-b61f-6909bc2bfc10
  Args:
    source: Frederica_of_Hanover
    type: :Woman
  AddTriple (aae9099d-314e-425f-8023-967dfdc2cfd2)
 Call ID: aae9099d-314e-425f-8023-967dfdc2cfd2
  Args:
    relation: :isSiblingOf
    target: Frederica_of_Hanover
    source: George_William_of_Hanover_and_Cumberland
  AssignClass (81da0aac-094a-40ad-be26-36e5ac59ce05)
 Call ID: 81da0aac-094a-40ad-be26-36e5ac59ce05
  Args:
    source: King_Paul_of_Greece
    type: :Man
  AddTriple (41465b24-a171-41ce-a5be-31944e852d78)
 Call ID: 41465b24-a171-41ce-a5be-31944e852d78
  Args:
    source: Frederica_of_Hanover
    relation: :hasRelation
    target: King_Paul_of_Greece
  AssignClass (b27a4309-5992-4919-b130-61962768009f)
 Call ID: b27a4309-5992-4919-b130-61962768009f
  Args:
    type: :Man
    source: Welf_of_Hanover
  AssignClass (02c22de2-5106-4abc-bf5c-b18b989af7ee)
 Call ID: 02c22de2-5106-4abc-bf5c-b18b989af7ee
  Args:
    type: :Man
    source: Georg_of_Hanover
  AssignClass (17614a90-8799-4bce-9efb-3b1d73a36772)
 Call ID: 17614a90-8799-4bce-9efb-3b1d73a36772
  Args:
    source: Friederike_of_Hanover
    type: :Woman
  AddTriple (9cfd44b2-0099-420c-a5f6-4e908c9f88d8)
 Call ID: 9cfd44b2-0099-420c-a5f6-4e908c9f88d8
  Args:
    relation: :hasFather
    target: George_William_of_Hanover_and_Cumberland
    source: Welf_of_Hanover
  AddTriple (103dc757-f018-47c0-927d-a8e3cdb49032)
 Call ID: 103dc757-f018-47c0-927d-a8e3cdb49032
  Args:
    target: Sophie_of_Greece_and_Denmark
    relation: :hasMother
    source: Welf_of_Hanover
  AddTriple (684d4717-ba5c-4f14-bf6e-30cd561cbde0)
 Call ID: 684d4717-ba5c-4f14-bf6e-30cd561cbde0
  Args:
    source: Georg_of_Hanover
    relation: :hasFather
    target: George_William_of_Hanover_and_Cumberland
  AddTriple (3904812d-d1b2-4f38-9cf5-f3caa2a4cd80)
 Call ID: 3904812d-d1b2-4f38-9cf5-f3caa2a4cd80
  Args:
    source: Georg_of_Hanover
    relation: :hasMother
    target: Sophie_of_Greece_and_Denmark
  AddTriple (5b4c431c-85bf-4c1e-924c-a94a28cbc990)
 Call ID: 5b4c431c-85bf-4c1e-924c-a94a28cbc990
  Args:
    relation: :hasFather
    target: George_William_of_Hanover_and_Cumberland
    source: Friederike_of_Hanover
  AddTriple (03dca47c-5781-4151-9589-8ff6b0aae1b1)
 Call ID: 03dca47c-5781-4151-9589-8ff6b0aae1b1
  Args:
    source: Friederike_of_Hanover
    target: Sophie_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (c9ae3d4c-ec53-4562-9267-7af45ec2ee06)
 Call ID: c9ae3d4c-ec53-4562-9267-7af45ec2ee06
  Args:
    type: :Man
    source: Prince_Andrew_of_Greece_and_Denmark
  AssignClass (efd8b6a1-4512-44f5-b3c4-fd96ee6428fc)
 Call ID: efd8b6a1-4512-44f5-b3c4-fd96ee6428fc
  Args:
    type: :Woman
    source: Princess_Alice_of_Battenberg
  AddTriple (ab768de9-f130-4b77-b93a-2781924d4c80)
 Call ID: ab768de9-f130-4b77-b93a-2781924d4c80
  Args:
    target: Prince_Andrew_of_Greece_and_Denmark
    relation: :hasFather
    source: Sophie_of_Greece_and_Denmark
  AddTriple (cd69f95a-58b8-4699-99e7-ea0826e446a7)
 Call ID: cd69f95a-58b8-4699-99e7-ea0826e446a7
  Args:
    source: Sophie_of_Greece_and_Denmark
    target: Princess_Alice_of_Battenberg
    relation: :hasMother
  Finish (07b148ff-05f9-45b3-a663-dff2997bf42f)
 Call ID: 07b148ff-05f9-45b3-a663-dff2997bf42f
  Args: