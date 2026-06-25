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
Ernst August von Hannover (German: Ernst August Albert Paul Otto Rupprecht Oskar Berthold Friedrich-Ferdinand Christian-Ludwig Prinz von Hannover Herzog zu Braunschweig und Lüneburg Königlicher Prinz von Großbritannien und Irland, lit.
'Ernest Augustus Albert Paul Otto Rupert Oscar Berthold Frederick-Ferdinand Christian-Louis, Prince of Hanover, Duke of Brunswick and Lüneburg, Royal Prince of Great Britain and Ireland'; born 26 February 1954) is the head of the House of Hanover, members of which reigned in Great Britain and Ireland from 1714 to 1901, the Kingdom of Hanover from 1814 to 1866 (electorate, from 1714 to 1814), and the Duchy of Brunswick from 1913 to 1918.
As the husband of Princess Caroline of Monaco, he is the brother-in-law of Albert II, Prince of Monaco.
Background and education

Ernst August was born in Hanover, the eldest son of Prince Ernest Augustus of Hanover (1914–1987), the former Hereditary Prince of Brunswick and his first wife, Princess Ortrud of Schleswig-Holstein-Sonderburg-Glücksburg (1925–1980).
He was christened Ernst August Albert Paul Otto Rupprecht Oskar Berthold Friedrich-Ferdinand Christian-Ludwig.
As the senior male-line descendant of George III of the United Kingdom, Ernst August is head of the House of Hanover.
Ancestry and heritage

The title of Prince of Great Britain and Ireland was recognised ad personam for Ernst August's father and his father's siblings by George V of the United Kingdom on 17 June 1914.
However, the title Royal Prince of Great Britain and Ireland had been entered into the family's German passports, together with the German titles, in 1914.
Ernst August continues to claim the style, "Royal Prince of Great Britain and Ireland".
However, in addition to being a German, Ernst August also has British citizenship since his father had successfully claimed it under the Sophia Naturalization Act 1705 (in the case of Attorney-General v. Prince Ernest Augustus of Hanover).
Since foreign royal titles can't be entered into a British passport, his father ended up being named Ernest Augustus Guelph, with the addition of His Royal Highness.
His children, including Ernst August, inherited British nationality under this name.
Marriage and family

First marriage

By a 24 August 1981 declaration issued by his father as the Head of House, pursuant to Chapter 3, §§ 3 and 5 of the House laws of 1836, Ernst August was authorised to marry dynastically, and did firstly marry, civilly in Pattensen on 28 August 1981 and religiously on 30 August 1981, Chantal Hochuli (born 2 June 1955 in Zürich), the daughter and heiress of a Swiss German architect and real estate developer, Johann Gustav "Hans" Hochuli (14 March 1912 in Switzerland – ?), and his German wife Rosmarie Lembeck (8 April 1921, in Essen, Rhine, Prussia, Germany – 12 December 2011).
They have two sons, Prince Ernst August (born 19 July 1983) and Prince Christian (born 1 June 1985).
Ernst August and Chantal Hochuli divorced in London on 23 October 1997.
In 1988, Ernst August unsuccessfully claimed custody of his infant nephew Otto Heinrich, son of his younger brother, Prince Ludwig Rudolph of Hanover.
Ludwig Rudolph placed a call to his brother in London, imploring him to take care of the couple's 10-month-old son, and shortly afterwards died by suicide.
Custody of Otto Heinrich was eventually awarded, contrary to the expressed wishes of Ludwig Rudolph as the surviving parent and Ernst August's legal efforts, to the child's maternal grandparents, Count Ariprand (1925–1996) and Countess Maria von Thurn und Valsassina-Como-Vercelli (born 1929), to be raised at their family seat, Bleiburg Castle in southern Austria.
Second marriage

Ernst August married secondly, civilly in Monaco on 23 January 1999, Princess Caroline of Monaco, who was at the time expecting their daughter, Princess Alexandra (born 20 July 1999).
As he was descended from George II of Great Britain in the male line, Ernst August sought and received permission to marry pursuant to the British Royal Marriages Act 1772, which would not be repealed until the Succession to the Crown Act 2013 took effect on 26 March 2015.
Similarly the Monégasque court officially notified the government of France of Caroline's marriage to Ernst August, receiving assurance that there was no objection in compliance with the (since defunct)
Moreover, in order for Caroline to retain her claim to the throne of Monaco and to transmit succession rights to future offspring, the couple were also obliged to obtain the approval of yet a third nation, in the form of official consent to the marriage of Caroline's father, Prince Rainier III, as the sovereign of Monaco.
After their marriage, Ernst August and Caroline moved to Le Mée-sur-Seine, France, where they had purchased an 18th-century manor house from their friend Karl Lagerfeld.
In 2009, it was reported that Caroline had separated from Ernst August and returned to live in Monaco.
Controversies

Assault on journalist

In 1999, Ernst August was accused of assaulting a journalist with an umbrella.
Turkish Pavilion

Ernst August was photographed urinating on the Turkish Pavilion at the Expo 2000 event in Hanover, causing a diplomatic incident and a complaint from the Turkish embassy accusing him of insulting the Turkish people.
Assault charge

In 2000, Ernst August was involved in a dispute with a German man, Joseph Brunnlehner, on the island of Lamu in Kenya.
Brunnlehner was the operator of a disco, and Ernst August allegedly assaulted him with a knuckleduster, upset about the noise coming from the disco.
Family property dispute

In 2004, Ernst August had signed over his German property to his elder son, including Marienburg Castle, the agricultural estate of Calenberg Castle, the "Princely House" at Herrenhausen Gardens in Hanover and some forests near Blankenburg Castle (Harz) which he had repurchased in former East Germany after the German reunification of 1990.
At the time, Ernst August's wealth was estimated as high as $250 million.
Since then, the younger Ernst August has taken over many representative tasks on behalf of his father.
In 2013, however, Ernst August was removed from the chairmanship of a family foundation based in Liechtenstein, the Duke of Cumberland Foundation, which holds the properties near Gmunden in Austria, the Hanovers' main residence in exile after 1866 when their Kingdom of Hanover was annexed by Prussia.
Instead, the younger Ernst August was put in charge, reportedly for negligence on part of his father, at the initiative of the foundation's trustee Prince Michael of Liechtenstein.
In 2017, Ernst August filed legal action to recover his chairmanship, and he intends to revoke the bestowal of his German property.
Assault on police

In 2020, under the influence of alcohol and medication, Ernst August injured a police officer at his hunting lodge in Austria.
Health

On Sunday, 3 April 2005, Ernst August was admitted to hospital with acute pancreatitis.
The next day, he fell into a deep coma, two days before the death of his father-in-law, Rainier III, Prince of Monaco.



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
  AssignClass (e0964ddc-7a7d-43d9-aff3-a26cca96c01f)
 Call ID: e0964ddc-7a7d-43d9-aff3-a26cca96c01f
  Args:
    source: Ernst_August_von_Hannover
    type: :Man
  AssignClass (599c096e-a5a6-406a-82a1-a88936fa2ffd)
 Call ID: 599c096e-a5a6-406a-82a1-a88936fa2ffd
  Args:
    source: Ernst_August_von_Hannover
    type: :Person
  AssignClass (bc532e1b-833f-481d-80fc-351ed84001f9)
 Call ID: bc532e1b-833f-481d-80fc-351ed84001f9
  Args:
    source: Prince_Ernest_Augustus_of_Hannover
    type: :Man
  AssignClass (9420e3de-e45e-40ec-bc31-512719de8c9e)
 Call ID: 9420e3de-e45e-40ec-bc31-512719de8c9e
  Args:
    source: Prince_Ernest_Augustus_of_Hannover
    type: :Person
  AssignClass (ef93bd90-466f-4a42-b4ac-51a522653943)
 Call ID: ef93bd90-466f-4a42-b4ac-51a522653943
  Args:
    source: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Woman
  AssignClass (79574eeb-545e-401d-8cba-0d4736836c7e)
 Call ID: 79574eeb-545e-401d-8cba-0d4736836c7e
  Args:
    source: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Person
  AddTriple (dc429646-f1cf-4950-ae59-48d952e837bd)
 Call ID: dc429646-f1cf-4950-ae59-48d952e837bd
  Args:
    source: Ernst_August_von_Hannover
    relation: :hasFather
    target: Prince_Ernest_Augustus_of_Hannover
  AddTriple (66515866-492c-4d45-b7ad-a930601dfd14)
 Call ID: 66515866-492c-4d45-b7ad-a930601dfd14
  Args:
    relation: :hasMother
    source: Ernst_August_von_Hannover
    target: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddLiteral (a5da6fa0-2b97-4185-8ab3-6382a55873cf)
 Call ID: a5da6fa0-2b97-4185-8ab3-6382a55873cf
  Args:
    literal_type: xsd:integer
    literal_value: 1954
    source: Ernst_August_von_Hannover
    relation: :hasBirthYear
  AddLiteral (fb90e059-ef3a-46bc-8bc3-8b4c87bb9cdb)
 Call ID: fb90e059-ef3a-46bc-8bc3-8b4c87bb9cdb
  Args:
    literal_value: 1914
    literal_type: xsd:integer
    source: Prince_Ernest_Augustus_of_Hannover
    relation: :hasBirthYear
  AddLiteral (9ae5c2f3-b3ad-47a6-bfd0-59d0f8b55ea1)
 Call ID: 9ae5c2f3-b3ad-47a6-bfd0-59d0f8b55ea1
  Args:
    literal_type: xsd:integer
    literal_value: 1987
    relation: :hasDeathYear
    source: Prince_Ernest_Augustus_of_Hannover
  AddLiteral (00beb654-6031-4cf8-824a-56214c1d1448)
 Call ID: 00beb654-6031-4cf8-824a-56214c1d1448
  Args:
    source: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1925
  AddLiteral (eb324111-9565-4981-b7c9-b1248fa27a28)
 Call ID: eb324111-9565-4981-b7c9-b1248fa27a28
  Args:
    relation: :hasDeathYear
    source: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    literal_type: xsd:integer
    literal_value: 1980
  AssignClass (a1d63ca4-3317-441b-8b1d-b5d55792aafd)
 Call ID: a1d63ca4-3317-441b-8b1d-b5d55792aafd
  Args:
    source: Chantal_Hochuli
    type: :Woman
  AssignClass (5cfc33b7-1322-4f5b-af84-b06c3221c395)
 Call ID: 5cfc33b7-1322-4f5b-af84-b06c3221c395
  Args:
    source: Chantal_Hochuli
    type: :Person
  AddTriple (b8b80dca-755d-43f1-9105-58462acad1a2)
 Call ID: b8b80dca-755d-43f1-9105-58462acad1a2
  Args:
    relation: :hasRelation
    source: Ernst_August_von_Hannover
    target: Chantal_Hochuli
  AddLiteral (9c26f32f-f6f6-4c60-8b71-bf29c394f690)
 Call ID: 9c26f32f-f6f6-4c60-8b71-bf29c394f690
  Args:
    literal_type: xsd:integer
    literal_value: 1981
    relation: :hasMarriageYear
    source: Ernst_August_von_Hannover
  AssignClass (f7f8427d-ad1e-4b87-87f1-691be3f55ac0)
 Call ID: f7f8427d-ad1e-4b87-87f1-691be3f55ac0
  Args:
    source: Prince_Ernst_August_Jr
    type: :Man
  AssignClass (331d59e4-9c91-4d41-9202-08830e5ec723)
 Call ID: 331d59e4-9c91-4d41-9202-08830e5ec723
  Args:
    source: Prince_Ernst_August_Jr
    type: :Person
  AssignClass (0845d0ff-c4df-4220-802e-c986f2ea2579)
 Call ID: 0845d0ff-c4df-4220-802e-c986f2ea2579
  Args:
    source: Prince_Christian
    type: :Man
  AssignClass (29ca2e8f-513e-4482-addb-5f1aee007c0a)
 Call ID: 29ca2e8f-513e-4482-addb-5f1aee007c0a
  Args:
    source: Prince_Christian
    type: :Person
  AddTriple (40c16b26-322f-400c-8134-4c12503a6b3e)
 Call ID: 40c16b26-322f-400c-8134-4c12503a6b3e
  Args:
    target: Prince_Ernst_August_Jr
    source: Ernst_August_von_Hannover
    relation: :hasSon
  AddTriple (6984f97e-915e-494b-bd63-667456f372cc)
 Call ID: 6984f97e-915e-494b-bd63-667456f372cc
  Args:
    target: Prince_Christian
    source: Ernst_August_von_Hannover
    relation: :hasSon
  AssignClass (ad349f24-7e4e-4f04-8d18-2e3c06b0588f)
 Call ID: ad349f24-7e4e-4f04-8d18-2e3c06b0588f
  Args:
    source: Prince_Ludwig_Rudolph_of_Hannover
    type: :Man
  AssignClass (de92948c-823e-4288-9c35-747b89d22f73)
 Call ID: de92948c-823e-4288-9c35-747b89d22f73
  Args:
    source: Prince_Ludwig_Rudolph_of_Hannover
    type: :Person
  AddTriple (318aef54-49f4-4e72-afe4-12ed79113f51)
 Call ID: 318aef54-49f4-4e72-afe4-12ed79113f51
  Args:
    source: Ernst_August_von_Hannover
    relation: :isBrotherOf
    target: Prince_Ludwig_Rudolph_of_Hannover
  AssignClass (dd6165dc-4dfa-443c-a8be-568c8b0e7cc5)
 Call ID: dd6165dc-4dfa-443c-a8be-568c8b0e7cc5
  Args:
    source: Otto_Heinrich
    type: :Man
  AssignClass (93552389-c3a2-4b24-bef7-4348ebfd4c23)
 Call ID: 93552389-c3a2-4b24-bef7-4348ebfd4c23
  Args:
    source: Otto_Heinrich
    type: :Person
  AddTriple (d8e5b721-7002-4631-b08b-8e474c53e84b)
 Call ID: d8e5b721-7002-4631-b08b-8e474c53e84b
  Args:
    target: Prince_Ludwig_Rudolph_of_Hannover
    source: Otto_Heinrich
    relation: :hasFather
  AssignClass (1eb373b2-42e8-4458-ae7e-ec98108cc570)
 Call ID: 1eb373b2-42e8-4458-ae7e-ec98108cc570
  Args:
    source: Princess_Caroline_of_Monaco
    type: :Woman
  AssignClass (1eca6d3e-c5ec-4197-983c-97bb66916f96)
 Call ID: 1eca6d3e-c5ec-4197-983c-97bb66916f96
  Args:
    source: Princess_Caroline_of_Monaco
    type: :Person
  AddTriple (f2f8b2ea-a96b-46c5-839b-37999ebee581)
 Call ID: f2f8b2ea-a96b-46c5-839b-37999ebee581
  Args:
    relation: :hasRelation
    source: Ernst_August_von_Hannover
    target: Princess_Caroline_of_Monaco
  AddLiteral (de536004-ba18-44db-a84b-38b59a741905)
 Call ID: de536004-ba18-44db-a84b-38b59a741905
  Args:
    relation: :hasMarriageYear
    source: Ernst_August_von_Hannover
    literal_type: xsd:integer
    literal_value: 1999
  AssignClass (3ba2e4a0-e576-448c-b18e-1b8cdf5618a2)
 Call ID: 3ba2e4a0-e576-448c-b18e-1b8cdf5618a2
  Args:
    source: Princess_Alexandra
    type: :Woman
  AssignClass (190d040a-21d8-40be-b818-18c884a9b10b)
 Call ID: 190d040a-21d8-40be-b818-18c884a9b10b
  Args:
    source: Princess_Alexandra
    type: :Person
  AddTriple (da7ee946-213a-4c7e-b5cf-842d5ebb9afe)
 Call ID: da7ee946-213a-4c7e-b5cf-842d5ebb9afe
  Args:
    target: Princess_Alexandra
    source: Ernst_August_von_Hannover
    relation: :hasDaughter
  AddTriple (00fd0daa-0c27-4810-8088-33006a3f60fc)
 Call ID: 00fd0daa-0c27-4810-8088-33006a3f60fc
  Args:
    target: Princess_Caroline_of_Monaco
    relation: :hasMother
    source: Princess_Alexandra
  AssignClass (4ac623ff-7dbe-434a-8dcf-d27184a3679a)
 Call ID: 4ac623ff-7dbe-434a-8dcf-d27184a3679a
  Args:
    source: Prince_Rainier_III
    type: :Man
  AssignClass (6103f3f0-2807-4c89-a684-8146057fdc9e)
 Call ID: 6103f3f0-2807-4c89-a684-8146057fdc9e
  Args:
    source: Prince_Rainier_III
    type: :Person
  AddTriple (2878850e-78fb-4324-a360-cc2b5707db0a)
 Call ID: 2878850e-78fb-4324-a360-cc2b5707db0a
  Args:
    source: Princess_Caroline_of_Monaco
    relation: :hasFather
    target: Prince_Rainier_III
  Finish (86b0a607-eaa4-4256-8db7-5817193deab2)
 Call ID: 86b0a607-eaa4-4256-8db7-5817193deab2
  Args: