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
Infanta Beatriz of Spain, Princess of Civitella-Cesi (Beatriz Isabel Federica Alfonsa Eugénie Cristina Maria Teresia Bienvenida Ladislàa de Borbón y Battenberg; 22 June 1909 – 22 November 2002) was a daughter of King Alfonso XIII of Spain and Victoria Eugenie of Battenberg, wife of Alessandro Torlonia, 5th Prince di Civitella-Cesi.
She was a paternal aunt of King Juan Carlos I.


Childhood

Born at the royal palace of La Granja, San Ildefonso near Segovia, Spain on 22 June 1909, Infanta Beatriz was the third child among the six surviving children of King Alfonso XIII of Spain and Victoria Eugenie of Battenberg.
She was named Beatriz after her maternal grandmother, Princess Beatrice of the United Kingdom, the youngest daughter of Queen Victoria; Isabel for her great-aunt, Infanta Isabel; Federica for Princess Frederica of Hanover in whose house her parents had become engaged; Alfonsa after her father; Eugenia for Empress Eugénie of the French, her mother's godmother, Cristina and Maria for Maria Christina of Austria, her paternal grandmother, Teresia after Empress Maria Theresa and Ladislaa after Ladislaus the Posthumous.
Infanta Beatriz was educated within the walls of the Palacio de Oriente by English nannies.
Infanta Beatriz and her sister Maria Cristina, two years her junior, yearned to go to private schools like the daughters of the nobility who frequented the palace as their playmates, but, following Spanish tradition, they were educated by governesses and private tutors.
Their parents placed great importance on outdoor exercise and Infanta Beatriz became fond of sports.
Early life

During the late 1920s, Infanta Beatriz and her sister Infanta Cristina presided at a number of official engagements while heading various institutions and sponsoring events.
Beatriz and her sister took nursing classes, helping twice a week at the Red Cross in Madrid from 9 am to 1 pm and from 3 to 7 pm.
Beatriz was president of the Red Cross in San Sebastián, working there during the royal family's summer vacation.
Beatriz, who resembled her Spanish relatives, was a brunette, tall and lean like her father.
In 1929, Infanta Beatriz turned twenty years old.
She fell in love with Miguel Primo de Rivera y Sáenz de Heredia, the youngest son of Miguel Primo de Rivera, who served as Prime Minister of Spain from 1923 to January 1930 with dictatorial powers.
Because Beatriz and her sister could be carriers of hemophilia, like their mother, King Alphonso XIII was reluctant to follow the tradition of finding husbands for them among Catholic royal princes.
The two sisters' constant companions were their cousins Alvaro, Alonso and Ataúlfo de Orleans y Borbón, the three sons of Infante Alfonso de Orleans y Borbón.
It was expected that Infanta Beatriz would marry Alonso and Maria Cristina, Alvaro, but nothing came out of it as their companionship was interrupted when the turbulent political situation in Spain derailed their lives.
Exile

The support that Alfonso XIII gave to the unpopular dictatorship of Primo de Rivera discredited the king.
Lacking the backing of the military forces, King Alfonso felt obliged to leave the country the same day, but did not abdicate, hoping to be called back to the throne.
Infanta Beatriz, her mother and her siblings, except for Infante Don Juan, who was away on assignment in the Spanish navy, were left behind in Madrid.
The marriage of their parents was unhappy and even in Spain the King and Queen led separate lives.
Queen Victoria Eugenie moved to London and later to Lausanne, Switzerland and the two infantas lived for a time with her.
In 1933 the king moved to Rapallo and as life was too isolated for Beatriz and her sister in Lausanne, they moved with their father to Italy.
At their daughters' insistence, King Alfonso moved to Rome and rented a house for them there.
Infanta Beatriz and her sister became friends with the members of the Italian royal family and quickly adapted to life in Rome.
Beatriz, who was spending summer vacation in Pörtschach am Wörthersee in Austria, was driving a car with her brother Gonzalo as passenger.
Marriage and issue

At the time of her brother's death, Infanta Beatriz was looking forward to her wedding.
While visiting Ostia, she was introduced to an Italian aristocrat, Alessandro Torlonia, 5th Prince di Civitella-Cesi.
Torlonia, who had inherited large estates from his father in 1933, was the son of Marino, 4th Prince di Civitella-Cesi and Mary Elsie Moore, an American heiress.
His family had acquired a fortune in the 18th and 19th centuries by administering the finances of the Vatican, receiving the title of Prince of Civitella-Cesi in 1803 from Pope Pius VII.
Although Don Alessandro was a prince, he did not belong to a reigning or formerly reigning dynasty, so Beatriz had to marry him morganatically, renouncing her rights of succession to the throne of Spain.
Alfonso XIII,
The wedding took place on 14 January 1935 at the Church of the Gesù with Beatriz wearing a 20-foot train, a coronet of orange blossom holding her veil in place, in the presence of King Alfonso, the King and Queen of Italy and some 52 princes of the blood royal.
Thousands of Spaniards traveled from Spain to give support to the deposed royal family in what became a political event.
However, neither Queen Victoria Eugenie nor Beatriz's eldest brother, Alfonso, Count of Covadonga, who were on bad terms with the King, attended the wedding.
Infanta Beatriz of Spain, Princess of Civitella-Cesi, and her husband had four children, eleven grandchildren and nineteen great-grandchildren:


Later life

Infanta Beatriz settled with her husband in the Palazzo Torlonia, a 16th-century Early Renaissance town house on Via della Conciliazione in Rome.
King Alfonso XIII died in 1941 and as the situation deteriorated in Italy during World War II, Infanta Beatriz with her family joined her siblings in Lausanne, spending the rest of the war close to their mother Queen Victoria Eugenie.
Beatriz returned to Italy after the war and dwelt there for the rest of her life.
In 1950, while staying with her brother Juan, in Estoril, Portugal, Infanta Beatriz obtained authorization from Francisco Franco to make a visit to Spain.
She returned to Spain on 25 August 1950 for the first time since her departure to exile almost twenty years earlier.
They stayed at the Ritz hotel in Madrid visiting the palace of la Granja, where the Infanta was born, and the Cathedral-Basilica of Our Lady of the Pillar in Zaragoza.
Infanta Beatriz was received with such a manifestation of support for the monarchy that after only a week, of a planned much longer visit, the government gave her only twenty four hours to leave the country.
Although the family tried to arrange a marriage for the Infanta's daughter, Sandra, with King Baudouin of Belgium, she caused her parents concern when in 1958 she married Clemente Lequio, a widower with a son, who was given the title "Count Lequio di Assaba" in 1963 by Umberto II of Italy.
Their son, Alesandro Lequio, moved to Spain in 1991 working initially for Fiat.
Married to the Italian model Antonia Dell’Atte, a muse in the late 1980s of Giorgio Armani, Alessandro Lequio quickly became a favorite of the Spanish jet set and tabloids, when, after his divorce, he began a relationship with Ana Obregón, a Spanish actress and television presenter.
Infanta Beatriz's eldest son, Marco, married three times and had three children, one in each marriage.
His eldest son, Don Giovanni Torlonia, is a well known designer.
Infanta Beatriz's second son, Marino, died unmarried in 1995 of HIV-related illnesses.
The youngest child, Olimpia, married in 1965 Paul-Annick Weiller (1933–1998), the first son of the aviator Paul-Louis Weiller of the Javal family.
Among their six children is Princess Sibilla of Luxembourg.
Infanta Beatriz remained very fond of Spain and supported the claims to the Spanish throne of her brother Don Juan.
In 1962, she joined the Spanish royal family in the celebration in Athens for the wedding of her nephew the future King Don Juan Carlos with Princess Sophia of Greece.
A femur fracture in 1973 never healed completely, affecting Infanta Beatriz's mobility for the rest of her life.
Her fragile health did not allow her to join her family at the ascension to the throne of King Juan Carlos, the wedding of the Infantas Elena and Cristina or the ceremonies for the return to Spain of the remains of her parents and siblings who had died in exile.
Nevertheless, Infanta Beatriz not only survived all of her siblings, but visited Spain again in 1998 to visit la Granja.
In 1999, the Infanta gave an interview with ¡Hola! Magazine, where she discussed her life and the years of the Royal Family's exile from Spain.
She made her last visit to Spain in 2001 to be with her sister-in-law Doña Maria and returned to the Palacio de la Magdalena, near Santander, where 70 years earlier she had spent her summer vacation for 17 consecutive years until 1930.
She died at her home in Palazzo Torlonia, Rome on 22 November 2002 at 93 years 5 months.
She was the last surviving legitimate child of Alfonso XIII and the last surviving legitimate grandchild of Alfonso XII of Spain.



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
  AssignClass (5d523d60-0902-43fc-99cf-06e39150da54)
 Call ID: 5d523d60-0902-43fc-99cf-06e39150da54
  Args:
    type: :Woman
    source: Infanta_Beatriz_of_Spain
  AssignClass (0c24fcd7-28e0-4f15-ad53-4631826b2bbb)
 Call ID: 0c24fcd7-28e0-4f15-ad53-4631826b2bbb
  Args:
    source: Infanta_Beatriz_of_Spain
    type: :Person
  AddLiteral (14e1e331-58d9-462c-a7dd-33cba2455443)
 Call ID: 14e1e331-58d9-462c-a7dd-33cba2455443
  Args:
    source: Infanta_Beatriz_of_Spain
    literal_value: 1909-06-22
    relation: :hasBirthYear
    literal_type: xsd:date
  AddLiteral (4aa690f0-e35e-4df2-b1b0-de8f3815227f)
 Call ID: 4aa690f0-e35e-4df2-b1b0-de8f3815227f
  Args:
    literal_type: xsd:date
    relation: :hasDeathYear
    literal_value: 2002-11-22
    source: Infanta_Beatriz_of_Spain
  AssignClass (a803c990-b9c4-442e-8dc5-88fba7bc61ce)
 Call ID: a803c990-b9c4-442e-8dc5-88fba7bc61ce
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Man
  AssignClass (9bad3a71-4d67-4e42-9b5a-f64a6deae67e)
 Call ID: 9bad3a71-4d67-4e42-9b5a-f64a6deae67e
  Args:
    type: :Person
    source: Alfonso_XIII_of_Spain
  AssignClass (eed2a08c-ad25-4998-aead-12721bc958e1)
 Call ID: eed2a08c-ad25-4998-aead-12721bc958e1
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Woman
  AssignClass (cc53281c-18cd-48f1-8ef4-0529caa1eb4d)
 Call ID: cc53281c-18cd-48f1-8ef4-0529caa1eb4d
  Args:
    type: :Person
    source: Victoria_Eugenie_of_Battenberg
  AddTriple (fb6a647a-9168-4818-b9c4-0d64820af9d4)
 Call ID: fb6a647a-9168-4818-b9c4-0d64820af9d4
  Args:
    relation: :hasFather
    source: Infanta_Beatriz_of_Spain
    target: Alfonso_XIII_of_Spain
  AddTriple (b3e43c32-c0ee-45c5-b146-dd798ddb7d01)
 Call ID: b3e43c32-c0ee-45c5-b146-dd798ddb7d01
  Args:
    relation: :hasMother
    target: Victoria_Eugenie_of_Battenberg
    source: Infanta_Beatriz_of_Spain
  AssignClass (bc910aab-157c-43ba-94fb-a571614e12c9)
 Call ID: bc910aab-157c-43ba-94fb-a571614e12c9
  Args:
    source: Alessandro_Torlonia
    type: :Man
  AssignClass (a6d107cc-f736-489a-834e-15a9858e5290)
 Call ID: a6d107cc-f736-489a-834e-15a9858e5290
  Args:
    type: :Person
    source: Alessandro_Torlonia
  AddTriple (64dcc69a-f4e5-4845-8a77-e46a62b343ce)
 Call ID: 64dcc69a-f4e5-4845-8a77-e46a62b343ce
  Args:
    target: Alessandro_Torlonia
    source: Infanta_Beatriz_of_Spain
    relation: :hasRelation
  AddLiteral (fba7fa02-d4d5-433f-bb77-aad94af4272b)
 Call ID: fba7fa02-d4d5-433f-bb77-aad94af4272b
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1935
    source: Infanta_Beatriz_of_Spain
  AssignClass (4492df4e-eebd-49d0-9c0c-649b29660f01)
 Call ID: 4492df4e-eebd-49d0-9c0c-649b29660f01
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (e561cbb8-adee-49f1-a05b-aa5ff380e5f2)
 Call ID: e561cbb8-adee-49f1-a05b-aa5ff380e5f2
  Args:
    type: :Person
    source: Juan_Carlos_I
  AddTriple (9a39e5c3-30b1-4869-8b00-8952e48782df)
 Call ID: 9a39e5c3-30b1-4869-8b00-8952e48782df
  Args:
    source: Infanta_Beatriz_of_Spain
    target: Juan_Carlos_I
    relation: :isAuntOf
  AssignClass (6e1a93cd-a4c1-4ccc-b6a4-3c40601f919a)
 Call ID: 6e1a93cd-a4c1-4ccc-b6a4-3c40601f919a
  Args:
    type: :Woman
    source: Maria_Cristina_of_Spain
  AssignClass (9e165126-551d-4d09-b870-97724cbf179a)
 Call ID: 9e165126-551d-4d09-b870-97724cbf179a
  Args:
    source: Maria_Cristina_of_Spain
    type: :Person
  AddTriple (8979cfb8-9236-4dba-9833-b13d71d9a0e7)
 Call ID: 8979cfb8-9236-4dba-9833-b13d71d9a0e7
  Args:
    source: Infanta_Beatriz_of_Spain
    target: Maria_Cristina_of_Spain
    relation: :isSisterOf
  AssignClass (741eed76-4948-43c9-b261-5794eb9e1550)
 Call ID: 741eed76-4948-43c9-b261-5794eb9e1550
  Args:
    source: Gonzalo_of_Spain
    type: :Man
  AssignClass (157a2350-d503-4ea8-96d2-883f3fa4d526)
 Call ID: 157a2350-d503-4ea8-96d2-883f3fa4d526
  Args:
    type: :Person
    source: Gonzalo_of_Spain
  AddTriple (66aa5223-3d71-4329-9200-3f3056383254)
 Call ID: 66aa5223-3d71-4329-9200-3f3056383254
  Args:
    target: Gonzalo_of_Spain
    source: Infanta_Beatriz_of_Spain
    relation: :hasBrother
  AssignClass (19d71385-173e-464d-8e97-2f371d9893cd)
 Call ID: 19d71385-173e-464d-8e97-2f371d9893cd
  Args:
    type: :Man
    source: Alfonso_Count_of_Covadonga
  AssignClass (8a2d589d-f4e6-4685-8ba4-cd212890341f)
 Call ID: 8a2d589d-f4e6-4685-8ba4-cd212890341f
  Args:
    type: :Person
    source: Alfonso_Count_of_Covadonga
  AddTriple (17d6554d-7903-47e8-83a7-45315f6cb33c)
 Call ID: 17d6554d-7903-47e8-83a7-45315f6cb33c
  Args:
    target: Alfonso_Count_of_Covadonga
    source: Infanta_Beatriz_of_Spain
    relation: :hasBrother
  AssignClass (46b4acb8-679b-4fd0-ae65-e0c08a54617a)
 Call ID: 46b4acb8-679b-4fd0-ae65-e0c08a54617a
  Args:
    source: Don_Juan_of_Spain
    type: :Man
  AssignClass (7df10c87-202d-4ad2-92bb-c8379cd64c83)
 Call ID: 7df10c87-202d-4ad2-92bb-c8379cd64c83
  Args:
    source: Don_Juan_of_Spain
    type: :Person
  AddTriple (46f689b4-df4a-40cd-b619-81372f1b5467)
 Call ID: 46f689b4-df4a-40cd-b619-81372f1b5467
  Args:
    relation: :hasBrother
    target: Don_Juan_of_Spain
    source: Infanta_Beatriz_of_Spain
  AssignClass (8beb90f1-6ed4-4417-83fe-a21e05969ee6)
 Call ID: 8beb90f1-6ed4-4417-83fe-a21e05969ee6
  Args:
    type: :Woman
    source: Sandra_Torlonia
  AssignClass (138073f0-907c-4532-b332-700638b990e1)
 Call ID: 138073f0-907c-4532-b332-700638b990e1
  Args:
    source: Sandra_Torlonia
    type: :Person
  AddTriple (426c00da-0d36-456d-87cf-b42de4e77811)
 Call ID: 426c00da-0d36-456d-87cf-b42de4e77811
  Args:
    source: Sandra_Torlonia
    target: Infanta_Beatriz_of_Spain
    relation: :hasMother
  AssignClass (ff82605d-1bb8-45b9-b994-b4f4610bb53d)
 Call ID: ff82605d-1bb8-45b9-b994-b4f4610bb53d
  Args:
    source: Clemente_Lequio
    type: :Man
  AssignClass (d83c36dd-26dc-4c91-9a23-f7b0d8fa5ac1)
 Call ID: d83c36dd-26dc-4c91-9a23-f7b0d8fa5ac1
  Args:
    type: :Person
    source: Clemente_Lequio
  AddTriple (66613e60-cfae-4c53-941e-e2303ec76b9c)
 Call ID: 66613e60-cfae-4c53-941e-e2303ec76b9c
  Args:
    target: Clemente_Lequio
    source: Sandra_Torlonia
    relation: :hasRelation
  AssignClass (b0bea334-3240-4c21-971b-1212147177e2)
 Call ID: b0bea334-3240-4c21-971b-1212147177e2
  Args:
    type: :Man
    source: Alesandro_Lequio
  AssignClass (6f5c83c2-9404-4732-a3bd-7eed8a394d76)
 Call ID: 6f5c83c2-9404-4732-a3bd-7eed8a394d76
  Args:
    source: Alesandro_Lequio
    type: :Person
  AddTriple (23380c99-503b-4513-b28f-6f00020137a1)
 Call ID: 23380c99-503b-4513-b28f-6f00020137a1
  Args:
    source: Alesandro_Lequio
    target: Sandra_Torlonia
    relation: :hasMother
  AddTriple (19e516b2-6a20-4096-8279-c3f160281b08)
 Call ID: 19e516b2-6a20-4096-8279-c3f160281b08
  Args:
    target: Clemente_Lequio
    source: Alesandro_Lequio
    relation: :hasFather
  AssignClass (947111b2-c426-4996-8b66-3eec2276a0ae)
 Call ID: 947111b2-c426-4996-8b66-3eec2276a0ae
  Args:
    type: :Man
    source: Marco_Torlonia
  AssignClass (f4e0b83c-2db3-46ed-ada6-92b6b41e2e4b)
 Call ID: f4e0b83c-2db3-46ed-ada6-92b6b41e2e4b
  Args:
    type: :Person
    source: Marco_Torlonia
  AddTriple (212655e4-5a2b-4105-8ec1-6d0d0ca2942b)
 Call ID: 212655e4-5a2b-4105-8ec1-6d0d0ca2942b
  Args:
    source: Marco_Torlonia
    target: Infanta_Beatriz_of_Spain
    relation: :hasMother
  AssignClass (48941efb-90b1-4aac-93fe-cc36774fa04d)
 Call ID: 48941efb-90b1-4aac-93fe-cc36774fa04d
  Args:
    source: Giovanni_Torlonia
    type: :Man
  AssignClass (2e458cac-e38d-43c6-8e02-bacfad45c837)
 Call ID: 2e458cac-e38d-43c6-8e02-bacfad45c837
  Args:
    type: :Person
    source: Giovanni_Torlonia
  AddTriple (c7269155-4a72-486e-8bbb-e724a7559a8c)
 Call ID: c7269155-4a72-486e-8bbb-e724a7559a8c
  Args:
    target: Marco_Torlonia
    source: Giovanni_Torlonia
    relation: :hasFather
  AssignClass (11a97379-f1a9-4da0-b2f4-a6bfa87738d3)
 Call ID: 11a97379-f1a9-4da0-b2f4-a6bfa87738d3
  Args:
    source: Marino_Torlonia_son
    type: :Man
  AssignClass (705086d0-da53-46e9-95b8-8184a9d50673)
 Call ID: 705086d0-da53-46e9-95b8-8184a9d50673
  Args:
    type: :Person
    source: Marino_Torlonia_son
  AddTriple (c2efc6c3-8051-4060-bad6-25ec26c3aff1)
 Call ID: c2efc6c3-8051-4060-bad6-25ec26c3aff1
  Args:
    target: Infanta_Beatriz_of_Spain
    source: Marino_Torlonia_son
    relation: :hasMother
  AssignClass (39c03f80-d808-451d-b507-249d8a010ad1)
 Call ID: 39c03f80-d808-451d-b507-249d8a010ad1
  Args:
    source: Olimpia_Torlonia
    type: :Woman
  AssignClass (e35c2885-e66c-4c51-9fe5-d44899cc0fca)
 Call ID: e35c2885-e66c-4c51-9fe5-d44899cc0fca
  Args:
    type: :Person
    source: Olimpia_Torlonia
  AddTriple (2d06d0c3-78c4-4828-86ad-eec2f9d5571b)
 Call ID: 2d06d0c3-78c4-4828-86ad-eec2f9d5571b
  Args:
    relation: :hasMother
    source: Olimpia_Torlonia
    target: Infanta_Beatriz_of_Spain
  AssignClass (7b384a8d-fb06-44e2-a499-3c2de3d6e2b3)
 Call ID: 7b384a8d-fb06-44e2-a499-3c2de3d6e2b3
  Args:
    source: Paul_Annick_Weiller
    type: :Man
  AssignClass (a4f76494-5686-4d94-a0cf-1e5ab3d0a9a9)
 Call ID: a4f76494-5686-4d94-a0cf-1e5ab3d0a9a9
  Args:
    source: Paul_Annick_Weiller
    type: :Person
  AddTriple (ef646624-7aa2-47b5-a426-fec346ee3ad1)
 Call ID: ef646624-7aa2-47b5-a426-fec346ee3ad1
  Args:
    relation: :hasRelation
    source: Olimpia_Torlonia
    target: Paul_Annick_Weiller
  AssignClass (848d5f01-56f3-4b37-8ea4-3db3fff126e4)
 Call ID: 848d5f01-56f3-4b37-8ea4-3db3fff126e4
  Args:
    type: :Woman
    source: Princess_Sibilla_of_Luxembourg
  AssignClass (3eaf8cb8-578a-4179-ad47-3a427b5c81a2)
 Call ID: 3eaf8cb8-578a-4179-ad47-3a427b5c81a2
  Args:
    type: :Person
    source: Princess_Sibilla_of_Luxembourg
  AddTriple (cb2c4e12-7485-4cff-ad4b-fb008905e9ea)
 Call ID: cb2c4e12-7485-4cff-ad4b-fb008905e9ea
  Args:
    relation: :hasMother
    target: Olimpia_Torlonia
    source: Princess_Sibilla_of_Luxembourg
  AddTriple (303c5993-0bf7-48ff-9326-904e06b313aa)
 Call ID: 303c5993-0bf7-48ff-9326-904e06b313aa
  Args:
    target: Paul_Annick_Weiller
    source: Princess_Sibilla_of_Luxembourg
    relation: :hasFather
  Finish (e0da115d-ea71-42b7-bf50-451d02d23d88)
 Call ID: e0da115d-ea71-42b7-bf50-451d02d23d88
  Args: