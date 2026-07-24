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
Frederik IX (Christian Frederik Franz Michael Carl Valdemar Georg; 11 March 1899 – 14 January 1972) was King of Denmark from 1947 to 1972.
Frederik was born into the House of Glücksburg during the reign of his great-grandfather King Christian IX.
He was the first child of Prince Christian of Denmark and Princess Alexandrine of Mecklenburg-Schwerin (later King Christian X and Queen Alexandrine).
In 1935, he married Princess Ingrid of Sweden.
During Nazi Germany's occupation of Denmark, Frederik acted as regent from 1942 until 1943 on behalf of his father, who had suffered a horseback riding accident in October 1942.
Frederik became king on his father's death in April 1947.
During Frederik's reign, Danish society changed rapidly, the welfare state was expanded and, as a consequence of the booming economy of the 1960s, women entered the labour market.
The modernization brought new demands on the monarchy and Frederik's role as a constitutional monarch.
Frederik died in 1972, and was succeeded by his eldest daughter, Margrethe II.


Birth and family

Frederik was born on 11 March 1899 at his parents' country residence, the Sorgenfri Palace, located on the shores of the small river Mølleåen in Kongens Lyngby north of Copenhagen on the island of Zealand in Denmark, during the reign of his great-grandfather King Christian IX.
His father was Prince Christian of Denmark (later King Christian X), the eldest son of Crown Prince Frederik and Princess Louise of Sweden (later King Frederik VIII and Queen Louise).
His mother was Alexandrine of Mecklenburg-Schwerin, the eldest daughter of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin and Grand Duchess Anastasia Mikhailovna of Russia.
The young prince had 21 godparents: Christian IX of Denmark (his paternal great-grandfather); Crown Prince Frederik of Denmark (his paternal grandfather); the Dowager Grand Duchess Anastasia of Mecklenburg-Schwerin (his maternal grandmother); Grand Duke Michael Nikolaevich of Russia (his maternal great-grandfather); Dowager Grand Duchess Marie of Mecklenburg-Schwerin (his maternal step-great-grandmother); Prince Carl of Denmark (his paternal uncle); Princess Thyra of Denmark (his paternal aunt); Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin (his maternal uncle); George I of Greece (his paternal great-uncle); Albert Edward, Prince of Wales (his paternal great-uncle by marriage); Ernest August, Duke of Cumberland (his paternal great-uncle by marriage); Grand Duke Alexander Mikhailovich of Russia (his maternal great-uncle); his first cousins once removed, Nicholas II of Russia, George, Duke of York, Prince George of Greece and Denmark and Georg Wilhelm, Hereditary Prince of Hanover; Crown Prince Constantine and Crown Princess Sophia of Greece (his first cousin once removed, and his wife); his paternal great-granduncles, Prince Johann of Schleswig-Holstein-Sonderburg-Glücksburg and King Oscar II of Sweden and Norway; and Crown Prince Gustaf and Crown Princess Victoria of Sweden (his first cousin twice removed and his wife).
Frederik's only sibling, Knud, was born one year after Frederik.
The family lived in apartments in Christian VIII's Palace at Amalienborg Palace in Copenhagen, in Sorgenfri Palace near the capital and in a summer residence, Marselisborg Palace in Aarhus in Jutland, which Frederik's parents had received as a wedding present from the people of Denmark in 1898.
Early life

Christian IX died on 29 January 1906, and Frederik's grandfather Crown Prince Frederik succeeded him as King Frederik VIII.
Frederik's father became crown prince, and Frederik moved up to second in line to the throne.
Just six years later, on 14 May 1912, King Frederik VIII died, and Frederik's father ascended the throne as King Christian X. Frederik himself became crown prince.
On 1 December 1918, as the Danish–Icelandic Act of Union recognized Iceland as a fully sovereign state in personal union with Denmark through a common monarch, Frederik also became crown prince of Iceland (where his name was officially spelled Friðrik).
Frederik was educated at the Royal Danish Naval Academy (breaking with Danish royal tradition by choosing a naval instead of an army career) and the University of Copenhagen.
In addition, with his love of music, Frederik was an able piano player and conductor.
Marriage and issue

In the 1910s, Alexandrine considered the two youngest daughters of her cousin Tsar Nicholas II, Grand Duchesses Maria and Anastasia Nikolaevna of Russia, as possible wives for Frederik until the execution of the Romanov family in 1918.
In 1922, Frederik was engaged to Princess Olga of Greece and Denmark, his double second cousin, through King Christian IX of Denmark and the other through Frederick Francis II.
They never wed.


Instead, on 15 March 1935, a few days after his 36th birthday, his engagement to Princess Ingrid of Sweden (1910–2000), a daughter of Crown Prince Gustaf Adolf (later King Gustaf VI Adolf of Sweden) and his first wife, Princess Margaret of Connaught, was announced.
Frederik and Ingrid were related in several ways.
In descent from Oscar I of Sweden and Leopold, Grand Duke of Baden, they were double third cousins.
In descent from Paul I of Russia, Frederik was a fourth cousin of Ingrid's mother.
Their wedding was one of the greatest media events of the day in Sweden in 1935, and among the wedding guests were the King and Queen of Denmark, the King and Queen of Belgium and the Crown Prince and Crown Princess of Norway.
Upon their return to Denmark, the couple were given Frederik VIII's Palace at Amalienborg Palace in Copenhagen as their primary residence and Gråsten Palace in Northern Schleswig as a summer residence.
Their daughters are:


Reign

From 1942 until 1943, Frederik acted as regent on behalf of his father who was temporarily incapacitated after a fall from his horse in October 1942.
On 20 April 1947, Christian X died, and Frederik succeeded to the throne.
Frederik IX's reign saw great change.
In other words, Denmark became a modern country, which meant new demands on the monarchy.
Changes to the Act of Succession

As King Frederik IX and Queen Ingrid had no sons, it was expected that the king's younger brother, Prince Knud, would inherit the throne, in accordance with Denmark's succession law (Royal Ordinance of 1853).
As a result, his eldest daughter, Margrethe, became heir presumptive.
Death and funeral

Shortly after Frederik delivered his New Year's address on 31 December 1971, he became ill with flu-like symptoms.
He was succeeded by his eldest daughter, Margrethe II.
Following his death, Frederik's coffin was transported to his home at Amalienborg Palace, where it stood until 18 January, when it was moved to the chapel at Christiansborg Palace.
There, the coffin was placed on castrum doloris, a ceremony largely unchanged since introduced at the burial of Frederik III in 1670, and the last remaining royal ceremony where the Danish Crown Regalia is used.
The gun carriage was pulled by 48 seamen and was escorted by honor guards from the Danish Army, Air Force, and Navy, as well as honor guards from France, Sweden, the United Kingdom, and the United States.
Queen Ingrid survived her husband by 28 years.
Legacy

In 1934, the Crown Prince Frederik Range in Greenland was named after him when it was first mapped by Sir Martin Lindsay during the British Trans-Greenland Expedition.
On 20 April 1982, a statue of King Frederik IX dressed in the uniform of an admiral was unveiled by the Copenhagen harbour on the 35th anniversary of his accession to the throne in 1947 and in the tenth year after his death.
Folktale

In the southern city of Sønderborg, Frederik has a dish named after himself.
The dish is called "Kong Fiddes livret" (King Frederik's favorite).
The name Fidde is a common diminutive nickname for people named Frederik in the southern parts of Denmark.
The dish is supposedly one that was regularly served to Frederik on his birthday at Gråsten Palace.



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
  AssignClass (8aae9730-9e11-4533-835d-da0815723baa)
 Call ID: 8aae9730-9e11-4533-835d-da0815723baa
  Args:
    type: :Man
    source: Frederik_IX
  AssignClass (e021e411-7cb6-4df9-84b7-09038ffe48e8)
 Call ID: e021e411-7cb6-4df9-84b7-09038ffe48e8
  Args:
    type: :Person
    source: Frederik_IX
  AddLiteral (9170422d-e5cf-4323-a747-59dbbcb6c488)
 Call ID: 9170422d-e5cf-4323-a747-59dbbcb6c488
  Args:
    literal_value: 1899
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Frederik_IX
  AddLiteral (9f69f402-108a-43fa-8bda-8ba893db605f)
 Call ID: 9f69f402-108a-43fa-8bda-8ba893db605f
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Frederik_IX
    literal_value: 1972
  AssignClass (078c11b5-333a-4a3c-b800-8e8f416663ea)
 Call ID: 078c11b5-333a-4a3c-b800-8e8f416663ea
  Args:
    type: :Man
    source: Christian_X
  AssignClass (da616977-7f16-4f8b-b60c-1f404d18c440)
 Call ID: da616977-7f16-4f8b-b60c-1f404d18c440
  Args:
    type: :Person
    source: Christian_X
  AssignClass (8f512c8a-ac01-4304-b033-9526814ea571)
 Call ID: 8f512c8a-ac01-4304-b033-9526814ea571
  Args:
    type: :Woman
    source: Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (b684e3b6-0901-4279-9271-66809cb4c495)
 Call ID: b684e3b6-0901-4279-9271-66809cb4c495
  Args:
    type: :Person
    source: Alexandrine_of_Mecklenburg-Schwerin
  AddTriple (86d51b47-aacd-4238-9d0c-092268c3f59e)
 Call ID: 86d51b47-aacd-4238-9d0c-092268c3f59e
  Args:
    relation: :hasFather
    target: Christian_X
    source: Frederik_IX
  AddTriple (e72b120d-3f69-44d3-90ac-1dac30227f7f)
 Call ID: e72b120d-3f69-44d3-90ac-1dac30227f7f
  Args:
    target: Alexandrine_of_Mecklenburg-Schwerin
    source: Frederik_IX
    relation: :hasMother
  AssignClass (85670779-533a-40c8-b734-d55a0b14bd27)
 Call ID: 85670779-533a-40c8-b734-d55a0b14bd27
  Args:
    type: :Woman
    source: Ingrid_of_Sweden
  AssignClass (dcbe7c17-febe-4dbb-8dc7-49975a0666d8)
 Call ID: dcbe7c17-febe-4dbb-8dc7-49975a0666d8
  Args:
    type: :Person
    source: Ingrid_of_Sweden
  AddTriple (cc8f103f-d655-4d60-9651-0cc770e49374)
 Call ID: cc8f103f-d655-4d60-9651-0cc770e49374
  Args:
    relation: :hasRelation
    target: Ingrid_of_Sweden
    source: Frederik_IX
  AddLiteral (19899c5d-6ec4-4c6a-a2a9-196ce45b9450)
 Call ID: 19899c5d-6ec4-4c6a-a2a9-196ce45b9450
  Args:
    literal_value: 1935
    source: Frederik_IX
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (9e6e55fa-7f70-439e-ad7a-9e5c330d6f7c)
 Call ID: 9e6e55fa-7f70-439e-ad7a-9e5c330d6f7c
  Args:
    type: :Man
    source: Knud
  AssignClass (f60b237a-5717-4351-a9ce-1e10d93ced4e)
 Call ID: f60b237a-5717-4351-a9ce-1e10d93ced4e
  Args:
    type: :Person
    source: Knud
  AddTriple (0aa0638f-de65-493b-a4d2-e8ac00cd315a)
 Call ID: 0aa0638f-de65-493b-a4d2-e8ac00cd315a
  Args:
    target: Frederik_IX
    source: Knud
    relation: :isBrotherOf
  AssignClass (741df904-2e5b-40da-9ce8-1499671de6e3)
 Call ID: 741df904-2e5b-40da-9ce8-1499671de6e3
  Args:
    type: :Woman
    source: Margrethe_II
  AssignClass (9cd4e09d-c2fb-400a-95a9-e353cb7f1b58)
 Call ID: 9cd4e09d-c2fb-400a-95a9-e353cb7f1b58
  Args:
    type: :Person
    source: Margrethe_II
  AddTriple (d147bb0e-f91c-40f0-b556-e401e5b61ab5)
 Call ID: d147bb0e-f91c-40f0-b556-e401e5b61ab5
  Args:
    relation: :isDaughterOf
    target: Frederik_IX
    source: Margrethe_II
  AssignClass (8b134398-6829-4e1c-bb93-5d912b4e339e)
 Call ID: 8b134398-6829-4e1c-bb93-5d912b4e339e
  Args:
    type: :Man
    source: Christian_IX
  AssignClass (e085256a-d7a4-4682-a075-0f218bcb4b1f)
 Call ID: e085256a-d7a4-4682-a075-0f218bcb4b1f
  Args:
    type: :Person
    source: Christian_IX
  AssignClass (c61f5513-4165-4ce6-be58-1a591345c454)
 Call ID: c61f5513-4165-4ce6-be58-1a591345c454
  Args:
    type: :Man
    source: Frederik_VIII
  AssignClass (48bcc405-9b3f-4ee5-93b7-9235c8866337)
 Call ID: 48bcc405-9b3f-4ee5-93b7-9235c8866337
  Args:
    type: :Person
    source: Frederik_VIII
  AssignClass (e80ae5a2-3a80-4715-b242-1dd7a6feed10)
 Call ID: e80ae5a2-3a80-4715-b242-1dd7a6feed10
  Args:
    type: :Woman
    source: Louise_of_Sweden
  AssignClass (ee06d98b-18be-48d0-9fe2-d80395125d5c)
 Call ID: ee06d98b-18be-48d0-9fe2-d80395125d5c
  Args:
    type: :Person
    source: Louise_of_Sweden
  AddTriple (ee8184f8-733f-42ec-be4b-907200b65a5a)
 Call ID: ee8184f8-733f-42ec-be4b-907200b65a5a
  Args:
    relation: :isFatherOf
    target: Christian_X
    source: Frederik_VIII
  AddTriple (89541d64-ac49-4e16-a769-6330c43fd629)
 Call ID: 89541d64-ac49-4e16-a769-6330c43fd629
  Args:
    source: Louise_of_Sweden
    target: Christian_X
    relation: :isMotherOf
  AddTriple (a1eaf094-61b7-4793-9d1f-2abe058516ed)
 Call ID: a1eaf094-61b7-4793-9d1f-2abe058516ed
  Args:
    relation: :isFatherOf
    source: Christian_IX
    target: Frederik_VIII
  AssignClass (53cdbfa1-a6bf-496b-9636-54db9ac999f5)
 Call ID: 53cdbfa1-a6bf-496b-9636-54db9ac999f5
  Args:
    type: :Man
    source: Frederick_Francis_III
  AssignClass (f2f53117-adea-49c7-98a1-c80de4f07a1c)
 Call ID: f2f53117-adea-49c7-98a1-c80de4f07a1c
  Args:
    type: :Person
    source: Frederick_Francis_III
  AssignClass (bb9ae3ed-f1c1-476f-b65b-ef506fa3f40d)
 Call ID: bb9ae3ed-f1c1-476f-b65b-ef506fa3f40d
  Args:
    type: :Woman
    source: Anastasia_Mikhailovna_of_Russia
  AssignClass (d391e088-ed94-431c-aa8e-60c3469d1f6e)
 Call ID: d391e088-ed94-431c-aa8e-60c3469d1f6e
  Args:
    type: :Person
    source: Anastasia_Mikhailovna_of_Russia
  AddTriple (583d80fd-4a6c-403c-8ae3-62a342bff44b)
 Call ID: 583d80fd-4a6c-403c-8ae3-62a342bff44b
  Args:
    relation: :isFatherOf
    source: Frederick_Francis_III
    target: Alexandrine_of_Mecklenburg-Schwerin
  AddTriple (a2129f86-5a01-4267-a483-6d74e8ae989f)
 Call ID: a2129f86-5a01-4267-a483-6d74e8ae989f
  Args:
    relation: :isMotherOf
    target: Alexandrine_of_Mecklenburg-Schwerin
    source: Anastasia_Mikhailovna_of_Russia
  AssignClass (bf4f4700-cbf6-42e2-a375-efacbb89c03e)
 Call ID: bf4f4700-cbf6-42e2-a375-efacbb89c03e
  Args:
    type: :Man
    source: Gustaf_VI_Adolf_of_Sweden
  AssignClass (d2b0fee1-03da-4ca4-bb21-c8a45bdd69a3)
 Call ID: d2b0fee1-03da-4ca4-bb21-c8a45bdd69a3
  Args:
    type: :Person
    source: Gustaf_VI_Adolf_of_Sweden
  AssignClass (4c2705cd-7756-4d56-8c83-d44d2d33f4f5)
 Call ID: 4c2705cd-7756-4d56-8c83-d44d2d33f4f5
  Args:
    type: :Woman
    source: Margaret_of_Connaught
  AssignClass (bf727341-2d21-4d7b-9ca6-97acbaa7f878)
 Call ID: bf727341-2d21-4d7b-9ca6-97acbaa7f878
  Args:
    type: :Person
    source: Margaret_of_Connaught
  AddTriple (b948028a-2804-4210-8abd-772c003fd370)
 Call ID: b948028a-2804-4210-8abd-772c003fd370
  Args:
    source: Gustaf_VI_Adolf_of_Sweden
    target: Ingrid_of_Sweden
    relation: :isFatherOf
  AddTriple (fad90c89-6ede-40fc-b507-e0bf4498cef0)
 Call ID: fad90c89-6ede-40fc-b507-e0bf4498cef0
  Args:
    target: Ingrid_of_Sweden
    source: Margaret_of_Connaught
    relation: :isMotherOf
  Finish (3c425fc8-9808-4f54-bf05-2fb2e0ee4231)
 Call ID: 3c425fc8-9808-4f54-bf05-2fb2e0ee4231
  Args: